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
from ..context_processors import *


class AuthContextProcessorTestCase(TestCase):
    def setUp(self):
        user_model = get_user_model()
        
        self.request = FakeRequest()
        self.request.user = user_model.objects.create(username="u")
        
        self.request_with_superuser = FakeRequest()
        self.request_with_superuser.user = user_model.objects.create_superuser("su", "su@su.it", "password")
        
        self.request_with_anonymous = FakeRequest()
        
    def test_obj_perm_wrapper_is_not_iterable(self):
        """Tests raising an error when try to iterate over "ObjPermWrapper".
        """
        data = auth(self.request)
        
        self.assertRaises(TypeError, lambda : [m for m in data['obj_perms']])
        
    def test_adding_context_variable(self):
        """Tests a new "obj_perms" variable is added to context.
        """
        data = auth(self.request)
        
        self.assertTrue("obj_perms" in data)
        
        data = auth(self.request_with_superuser)
        
        self.assertTrue("obj_perms" in data)
        
        data = auth(self.request_with_anonymous)
        
        self.assertTrue("obj_perms" in data)
        
    def test_retrieving_obj_perms_from_anonymous_user(self):
        """Tests retrieving obj perms for anonymous user.
        """
        data = auth(self.request_with_anonymous)
        
        self.assertFalse(data['obj_perms']['core'])
        self.assertEqual(data['obj_perms']['core'], [])
        
    def test_retrieving_obj_perms_from_superuser(self):
        """Tests retrieving obj perms for superuser.
        """        
        data = auth(self.request_with_superuser)
        
        obj_perms = data['obj_perms']
        self.assertTrue(data['obj_perms']['core'])
        
        self.assertEqual(
            obj_perms['core']['change_user'],
            [self.request.user.pk, self.request_with_superuser.user.pk]
        )
        
        self.assertEqual(
            obj_perms['core']['view_user'],
            [self.request.user.pk, self.request_with_superuser.user.pk]
        )
        
        self.assertEqual(
            obj_perms['core']['delete_user'],
            [self.request.user.pk, self.request_with_superuser.user.pk]
        )
        
    def test_retrieving_obj_perms(self):
        """Tests retrieving obj perms of request's user from "obj_perms" var.
        """
        data = auth(self.request)
        obj_perms = data['obj_perms']
        
        self.assertTrue(obj_perms['core'])
        
        self.assertEqual(
            obj_perms['core']['change_user'],
            [self.request.user.pk]
        )
        
        self.assertEqual(
            obj_perms['core']['view_user'],
            [self.request.user.pk]
        )
        
        self.assertEqual(
            obj_perms['core']['delete_user'],
            [self.request.user.pk]
        )
        
    def test_retrieving_invalid_obj_perms(self):
        """Tests retrieving invalid obj perms of request's user.
        """
        data = auth(self.request)
        obj_perms = data['obj_perms']
        
        self.assertEqual(
            obj_perms['core']['invalid_perm_name'],
            []
        )
        
        self.assertFalse(obj_perms['core']['invalid_perm_name'])
        
    def test_repr_obj_perms(self):
        """Tests string representation of obj perms.
        """
        data = auth(self.request)
        obj_perms = data['obj_perms']
        
        self.assertEqual(
            "%s" % obj_perms['core']['view_user'],
            "[1]"
        )
        
    def test_repr_module_obj_perms(self):
        """Tests string representation of module obj perm list.
        """
        data = auth(self.request)
        obj_perms = data['obj_perms']
        
        self.assertEqual(
            "%s" % obj_perms['core'],
            repr(['core.view_user.1', 'core.change_user.1', 'core.delete_user.1'])
        )
        
    def test_repr_module_obj_perms_for_superuser(self):
        """Tests string representation of module obj perm list (with superuser).
        """
        data = auth(self.request_with_superuser)
        obj_perms = data['obj_perms']
        
        self.assertEqual(
            "%s" % obj_perms['core'],
            repr(['core.view_user.1', 'core.view_user.2', 'core.change_user.1', 'core.change_user.2', 'core.delete_user.1', 'core.delete_user.2'])
        )
