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
from django.contrib.auth.hashers import make_password

from . import *
from ..models import ObjectPermission, User, Group
      
  
class UserManagerTestCase(TestCase):
    def test_create_user_helper(self):
        """Test "create_user" helper function.
        """
        u = User.objects.create_user("u1", "u@u.it", "password")
        
        self.assertTrue(isinstance(u, User))
        self.assertEqual(u.username, "u1")
        self.assertEqual(u.email, "u@u.it")
        self.assertEqual(u.is_active, True)
        self.assertEqual(u.is_superuser, False)
        self.assertEqual(u.is_staff, False)
        self.assertTrue(u.check_password("password"))
        
    def test_create_superuser_helper(self):
        """Test "create_superuser" helper function.
        """
        u = User.objects.create_superuser("su", "su@u.it", "superpassword")
        
        self.assertTrue(isinstance(u, User))
        self.assertEqual(u.username, "su")
        self.assertEqual(u.email, "su@u.it")
        self.assertEqual(u.is_active, True)
        self.assertEqual(u.is_superuser, True)
        self.assertEqual(u.is_staff, True)
        self.assertTrue(u.check_password("superpassword"))
        
    def test_fail_user_creation_without_username(self):
        """Test failure of "create_*user" helpers when no username is given.
        """
        try:
            User.objects.create_user(None, "su@u.it", "superpassword")
            self.fail()
        except ValueError:
            pass
            
        try:
            User.objects.create_superuser(None, "su@u.it", "superpassword")
            self.fail()
        except ValueError:
            pass

class PermissionManagerTestCase(TestCase):
    def setUp(self):
        self.p, n = Permission.objects.get_or_create_by_natural_key("view_user", auth_app, "user")
        
    def test_get_or_create_perm_by_natural_key(self):
        """Tests "PermissionManager.get_or_create_by_natural_key" method.
        """
        p, n = Permission.objects.get_or_create_by_natural_key("view_user", auth_app, "user")
        
        self.assertFalse(n)
        self.assertEqual(p, self.p)
        self.assertEqual(p.content_type.app_label, auth_app)
        self.assertEqual(p.content_type.model, "user")
        self.assertEqual(p.codename, "view_user")
        
    def test_get_perm_by_uid(self):
        """Tests "PermissionManager.get_by_uid" method.
        """
        p = Permission.objects.get_by_uid("%s.view_user" % auth_app)
        
        self.assertEqual(p, self.p)
        self.assertEqual(p.content_type.app_label, auth_app)
        self.assertEqual(p.content_type.model, "user")
        self.assertEqual(p.codename, "view_user")
        
    def test_get_or_create_perm_by_uid(self):
        """Tests "PermissionManager.get_or_createby_uid" method.
        """
        p, n = Permission.objects.get_or_create_by_uid("%s.view_user" % auth_app)
        
        self.assertFalse(n)
        self.assertEqual(p, self.p)
        self.assertEqual(p.content_type.app_label, auth_app)
        self.assertEqual(p.content_type.model, "user")
        self.assertEqual(p.codename, "view_user")

class ObjectPermissionManagerTestCase(TestCase):
    def setUp(self):
        self.u1 = User.objects.create(username="u1")
        self.u2 = User.objects.create(username="u2")
        self.g = Group.objects.create(name="my_group")
        self.op1, n = ObjectPermission.objects.get_or_create_by_natural_key("view_user", auth_app, "user", self.u1.pk)
        self.op2, n = ObjectPermission.objects.get_or_create_by_natural_key("view_user", auth_app, "user", self.u2.pk)
        
        self.g.user_set.add(self.u1)
        self.g.objectpermissions.add(self.op2)
        self.u1.objectpermissions.add(self.op1)
        self.u2.objectpermissions.add(self.op2)
        
    def test_get_perm_by_empty_object(self):
        """Tests "ObjectPermissionManager.get_by_object" method (without obj).
        """
        self.assertQuerysetEqual(
            ObjectPermission.objects.get_by_object(None),
            list(map(repr, ObjectPermission.objects.all())),
            ordered=False
        )
        
    def test_get_perm_by_object(self):
        """Tests "ObjectPermissionManager.get_by_object" method (with obj).
        """
        self.assertQuerysetEqual(
            ObjectPermission.objects.get_by_object(self.u2),
            [
                repr(ObjectPermission.objects.get_by_natural_key("view_user", auth_app, "user", self.u2.pk)),
                repr(ObjectPermission.objects.get_by_natural_key("change_user", auth_app, "user", self.u2.pk)),
                repr(ObjectPermission.objects.get_by_natural_key("delete_user", auth_app, "user", self.u2.pk)),
            ],
            ordered=False
        )
        
    def test_get_perm_by_natural_key(self):
        """Tests "ObjectPermissionManager.get_by_natural_key" method.
        """
        op = ObjectPermission.objects.get_by_natural_key("view_user", auth_app, "user", self.u1.pk)
        
        self.assertEqual(op, self.op1)
        self.assertEqual(op.perm.content_type.app_label, auth_app)
        self.assertEqual(op.perm.content_type.model, "user")
        self.assertEqual(op.perm.codename, "view_user")
        self.assertEqual(op.object_id, 1)
        
    def test_get_or_create_perm_by_natural_key(self):
        """Tests "ObjectPermissionManager.get_or_create_by_natural_key" method.
        """
        op, n = ObjectPermission.objects.get_or_create_by_natural_key("view_user", auth_app, "user", self.u1.pk)
        
        self.assertFalse(n)
        self.assertEqual(op, self.op1)
        self.assertEqual(op.perm.content_type.app_label, auth_app)
        self.assertEqual(op.perm.content_type.model, "user")
        self.assertEqual(op.perm.codename, "view_user")
        self.assertEqual(op.object_id, 1)
        
    def test_get_perm_by_uid(self):
        """Tests "ObjectPermissionManager.get_by_uid" method.
        """
        op = ObjectPermission.objects.get_by_uid("%s.view_user.%s" % (auth_app, self.u1.pk))
        
        self.assertEqual(op, self.op1)
        self.assertEqual(op.perm.content_type.app_label, auth_app)
        self.assertEqual(op.perm.content_type.model, "user")
        self.assertEqual(op.perm.codename, "view_user")
        self.assertEqual(op.object_id, 1)
        
    def test_get_or_create_perm_by_uid(self):
        """Tests "ObjectPermissionManager.get_or_create_by_uid" method.
        """
        op, n = ObjectPermission.objects.get_or_create_by_uid("%s.view_user.%s" % (auth_app, self.u1.pk))
        
        self.assertFalse(n)
        self.assertEqual(op, self.op1)
        self.assertEqual(op.perm.content_type.app_label, auth_app)
        self.assertEqual(op.perm.content_type.model, "user")
        self.assertEqual(op.perm.codename, "view_user")
        self.assertEqual(op.object_id, 1)

    def test_get_all_permissions(self):
        """Tests "ObjectPermissionManager.get_all_permissions" method.
        """
        all_perms_u1 = ObjectPermission.objects.get_all_permissions(self.u1).filter(perm__codename="view_user")
        
        self.assertQuerysetEqual(
            all_perms_u1,
            [repr(r) for r in (self.op1, self.op2)],
            ordered=False
        )
        
        all_perms_u2 = ObjectPermission.objects.get_all_permissions(self.u2).filter(perm__codename="view_user")
        
        self.assertQuerysetEqual(
            all_perms_u2,
            [repr(self.op2)],
            ordered=False
        )
