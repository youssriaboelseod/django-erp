#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""This file is part of the django ERP project.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

__author__ = 'Emanuele Bertoldi <emanuele.bertoldi@gmail.com>'
__copyright__ = 'Copyright (c) 2013-2015, django ERP Team'
__version__ = '0.0.5'

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend as DjangoModelBackend

from .models import *

class ModelBackend(DjangoModelBackend):
    """A proxy model-level backend.
    
    NOTE: the purpose of this backend is a better integration with object-level
    permissions. By default, "django.contrib.auth.backends.ModelBackend" will
    return "False" when "has_perm" is invoked passing an object instance. This
    proxy backend, instead, will return "True" if the user has the correct
    model-level permission. The idea is that a model-level permission is a
    generic permission over all instances, so if the user has a permission on a
    model class, this means he has a permission over all its instances.    
    """
    def get_group_permissions(self, user_obj, obj=None):
        return super(ModelBackend, self).get_group_permissions(user_obj)
        
    def get_all_permissions(self, user_obj, obj=None):
        return super(ModelBackend, self).get_all_permissions(user_obj)

    def has_perm(self, user_obj, perm, obj=None):
        if isinstance(perm, Permission):
            perm = perm.uid
        return super(ModelBackend, self).has_perm(user_obj, perm)

class ObjectPermissionBackend(object):
    """Backend which enables support for row/object-level permissions.
    
    NOTE: this backend only handles row/object-level permissions. It must works
    in conjunction which Django's model backend, not as a replacement. In fact,
    if a user has only model-level permissions over a certain model (but no
    row/object-level ones for that particular model instance) this backend's
    "has_perm" method will return a negative response.
    """
    supports_object_permissions = True
    supports_anonymous_user = True
    supports_inactive_user = True

    def authenticate(self, username, password):
        # This backend doesn't handle user authentication.
        return None

    def get_user_permissions(self, user_obj, obj=None):
        """Returns all and only the object perms granted to the user_obj itself.
        """
        if True: # not hasattr(user_obj, '_user_obj_perm_cache'):
            user_obj._user_obj_perm_cache = set([p.uid for p in user_obj.objectpermissions.get_by_object(obj)])
        return user_obj._user_obj_perm_cache

    def get_group_permissions(self, user_obj, obj=None):
        """Returns all and only the object perms granted to the groups of the given user_obj.
        """
        if True: # not hasattr(user_obj, '_group_obj_perm_cache'):
            perms = ObjectPermission.objects.get_group_permissions(user_obj, obj)
            perms = perms.values_list('perm__content_type__app_label', 'perm__codename', 'object_id').order_by()
            user_obj._group_obj_perm_cache = set(["%s.%s.%s" % (ct, name, obj_id) for ct, name in perms])
        return user_obj._group_obj_perm_cache

    def get_all_permissions(self, user_obj, obj=None):
        """Returns all and only the object perms granted to the given user_obj.
        """
        if user_obj.is_anonymous():
            return set()
        if True: # not hasattr(user_obj, '_obj_perm_cache'):
            user_obj._obj_perm_cache = self.get_user_permissions(user_obj, obj)
            user_obj._obj_perm_cache.update(self.get_group_permissions(user_obj, obj))
        return user_obj._obj_perm_cache

    def has_perm(self, user_obj, perm, obj=None):
        """This method checks if the user_obj has perm on obj.
        """
        if user_obj.is_superuser:
            return True

        if not user_obj.is_active:
            return False

        if obj is None:
            return False

        if isinstance(perm, Permission):
            perm = perm.uid

        perms = "%s.%s" % (perm, obj.pk) in self.get_all_permissions(user_obj, obj)
        
        # Fallback to model-level permissions.
        #if not perms:
        #    from django.contrib.auth.backends import ModelBackend
        #    perms = ModelBackend().has_perm(user_obj, perm)
        
        return perms
