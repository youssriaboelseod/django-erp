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


from django.test import TestCase, RequestFactory
from django.test.utils import override_settings
from django.shortcuts import render_to_response
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.conf import settings

from ..models import Permission, ObjectPermission
from ..decorators import *


def _get_user(request, *args, **kwargs):
    pk = kwargs.get("pk")
    user = None
    if pk:
        user = get_user_model().objects.get(pk=pk)
    return user
    
def _get_perm_name(request, *args, **kwargs):
    return "core.view_user"


@obj_permission_required("core.view_user", _get_user)        
def test_decorator_view(request, *args, **kwargs):
    return render_to_response('index.html')

@obj_permission_required(_get_perm_name, _get_user)        
def test_decorator_view2(request, *args, **kwargs):
    return render_to_response('index.html')


@override_settings(
    LOGIN_REQUIRED_URLS_EXCEPTIONS=(r'/(.*)$',),
    TEMPLATE_DIRS=("%s/core/tests/templates" % settings.PROJECT_PATH,),
)
class ObjPermissionRequiredTestCase(TestCase):    
    def setUp(self):
        self.factory = RequestFactory()
        self.user_model = get_user_model()
        
        # Please note that "User.objects.create_user" is different from
        # "User.objects.create" because it stores the hash of given password.
        self.u1 = self.user_model.objects.create_user("u1", "u1@u.it", "password")
        self.u2 = self.user_model.objects.create_user("u2", "u@u.it", "password")
        self.u3 = self.user_model.objects.create_user("u3", "u@u.it", "password")
        self.u4 = self.user_model.objects.create_user("u4", "u@u.it", "password")
        
        self.perm, n = Permission.objects.get_or_create_by_natural_key("view_user", "core", "user")
        self.obj_perm, n = ObjectPermission.objects.get_or_create_by_natural_key("view_user", "core", "user", self.u3.pk)
        
        self.u1.user_permissions.add(self.perm)        
        self.u2.objectpermissions.add(self.obj_perm)
        
    def test_decorator_with_anonymous_user(self):
        """Tests an anonymous user should not pass the decorator's test.
        """
        request = self.factory.get('/view_user/')
        request.user = AnonymousUser()
        
        response = test_decorator_view(request)
        
        self.assertEqual(response.status_code, 302)
        
    def test_get_perm_by_string_without_object(self):
        """Tests the decorator passing only the perm name by string (no obj).
        
        In this case it looks for a table-permission, instead of row-permission.
        """
        request = self.factory.get('/view_user/')
        request.user = self.u1
        
        response = test_decorator_view(request)
        
        self.assertEqual(response.status_code, 200)
        
        request.user = self.u2
        
        response = test_decorator_view(request)
        
        self.assertEqual(response.status_code, 302)
        
    def test_get_perm_by_string_with_object(self):
        """Tests the decorator passing only the perm name by string (with obj).
        """
        request = self.factory.get('/view_user/')
        request.user = self.u1
        
        response = test_decorator_view(request, pk=self.u3.pk)
        
        self.assertEqual(response.status_code, 200)
        
        request.user = self.u4
        
        response = test_decorator_view(request, pk=self.u3.pk)
        
        self.assertEqual(response.status_code, 302)
        
    def test_get_obj_perm_by_string_with_object(self):
        """Tests the decorator passing only the obj perm name by string (with obj).
        """
        request = self.factory.get('/view_user/')
        request.user = self.u2
        
        response = test_decorator_view(request, pk=self.u3.pk)
        
        self.assertEqual(response.status_code, 200)
        
        request.user = self.u4
        
        response = test_decorator_view(request, pk=self.u3.pk)
        
        self.assertEqual(response.status_code, 302)
        
    def test_fail_perm_by_string_with_object(self):
        """Tests failure of decorator passing perm name by string (with obj).
        """
        request = self.factory.get('/view_user/')
        request.user = self.u2
        
        response = test_decorator_view(request, pk=self.u1.pk)
        
        self.assertEqual(response.status_code, 302)
        
    def test_get_obj_perm_by_callable_with_object(self):
        """Tests the decorator passing a callable for obj perm name (with obj).
        """
        request = self.factory.get('/view_user/')
        request.user = self.u2
        
        response = test_decorator_view2(request, pk=self.u3.pk)
        
        self.assertEqual(response.status_code, 200)
        
    def test_fail_obj_perm_by_callable_with_object(self):
        """Tests failure of decorator passing a callable for obj perm name (with obj).
        """
        request = self.factory.get('/view_user/')
        request.user = self.u2
        
        response = test_decorator_view2(request, pk=self.u1.pk)
        
        self.assertEqual(response.status_code, 302)
