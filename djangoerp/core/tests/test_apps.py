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


from django.test import TestCase
from django.contrib.auth import get_user_model

from . import *
from ..models import Permission, Group
from ..apps import *


class AppConfigTestCase(TestCase):        
    def test_user_has_perms_on_itself(self):
        """Tests obj permissions to itself must be auto-added to user.
        """
        u1, n = get_user_model().objects.get_or_create(username="u1")
        
        self.assertTrue(ob.has_perm(u1, "%s.view_user" % auth_app, u1))
        self.assertTrue(ob.has_perm(u1, "%s.change_user" % auth_app, u1))
        self.assertTrue(ob.has_perm(u1, "%s.delete_user" % auth_app, u1))
        
    def test_create_contenttype_view_permission(self):
        """Tests a view permission must be auto-created on new contenttypes. 
        """
        from django.contrib.contenttypes.models import ContentType

        model_name = "dog"
        codename = "view_%s" % model_name
        
        self.assertEqual(ContentType.objects.filter(model=model_name).count(), 0)
        self.assertEqual(Permission.objects.filter(codename=codename).count(), 0)
        
        ContentType.objects.get_or_create(model=model_name, app_label=model_name)
        
        self.assertEqual(Permission.objects.filter(codename=codename).count(), 1)
        
    def test_assign_new_users_to_users_group(self):
        """Tests each new user must be assigned to "users" group.
        
        This is valid only if users are created NOT by the admin interface
        (i.e. registration).
        """
        u2, n = get_user_model().objects.get_or_create(username="u2")
        
        self.assertTrue(n)
        self.assertEqual(
            u2.groups.filter(name="users").exists(),
            True
        )

        # Only new created users are associated to "users" group.
        u2.groups.remove(Group.objects.get(name="users"))
        u2.save()

        self.assertEqual(
            u2.groups.filter(name="users").exists(),
            False
        )
