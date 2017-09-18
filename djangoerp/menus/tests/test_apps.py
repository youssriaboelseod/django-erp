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

from ..models import *
from ..utils import *


class AppConfigTestCase(TestCase):
    def test_initial_fixture_installation(self):
        """Tests installation of initial fixture.
        """
        from djangoerp.core.models import Group, Permission
        
        # Menus.
        main_menu, is_new = Menu.objects.get_or_create(slug="main")
        self.assertTrue(main_menu)
        self.assertFalse(is_new)
    
        user_area_not_logged_menu, is_new = Menu.objects.get_or_create(slug="user_area_not_logged")
        self.assertTrue(user_area_not_logged_menu)
        self.assertFalse(is_new)
    
        user_area_logged_menu, is_new = Menu.objects.get_or_create(slug="user_area_logged")
        self.assertTrue(user_area_logged_menu)
        self.assertFalse(is_new)
    
        user_detail_actions, is_new = create_detail_actions(get_user_model())
        self.assertTrue(user_detail_actions)
        self.assertFalse(is_new)
    
        user_detail_navigation, is_new = create_detail_navigation(get_user_model())
        self.assertTrue(user_detail_navigation)
        self.assertFalse(is_new)
        
        # Links.
        my_dashboard_link, is_new = Link.objects.get_or_create(slug="my-dashboard")
        self.assertTrue(my_dashboard_link)
        self.assertFalse(is_new)
        
        login_link, is_new = Link.objects.get_or_create(slug="login")
        self.assertTrue(login_link)
        self.assertFalse(is_new)
        
        administration_link, is_new = Link.objects.get_or_create(slug="administration")
        self.assertTrue(administration_link)
        self.assertFalse(is_new)
        
        logout_link, is_new = Link.objects.get_or_create(slug="logout")
        self.assertTrue(logout_link)
        self.assertFalse(is_new)
        
        user_edit_link, is_new = Link.objects.get_or_create(slug="user-edit")
        self.assertTrue(user_edit_link)
        self.assertFalse(is_new)
        
        user_delete_link, is_new = Link.objects.get_or_create(slug="user-delete")
        self.assertTrue(user_delete_link)
        self.assertFalse(is_new)
        
        # Perms.
        users_group, is_new = Group.objects.get_or_create(name="users")
        
        self.assertTrue(user_edit_link.only_with_perms.get_by_natural_key("change_user", "core", "user"))
        self.assertTrue(users_group.permissions.get_by_natural_key("add_link", "menus", "link"))
