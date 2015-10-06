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
from ..models import *
from ..utils import *
from ..signals import *
        
class SignalTestCase(TestCase):
    def test_bookmarks_auto_creation_for_users(self):
        """Tests a bookmarks list must be auto-created for new users.
        """
        self.assertEqual(Menu.objects.filter(slug="user_1_bookmarks").count(), 0)
        
        u1 = get_user_model().objects.create(username="u1")
        
        self.assertEqual(Menu.objects.filter(slug="user_1_bookmarks").count(), 1)
        
    def test_bookmarks_stop_auto_creation(self):
        """Tests disabling bookmarks list auto-creation.
        """
        user_model = get_user_model()
        
        self.assertEqual(Menu.objects.filter(slug="user_2_bookmarks").count(), 0)
        
        manage_bookmarks(user_model, False) # Disable auto-creation.
        
        u2 = user_model.objects.create(username="u2")
        
        self.assertEqual(Menu.objects.filter(slug="user_2_bookmarks").count(), 0)

        manage_bookmarks(user_model) # Enable auto-creation.
        
    def test_manage_author_permissions_on_bookmarks(self):
        """Tests that "manage_author_permissions" auto-generate perms for author. 
        """        
        u1, n = get_user_model().objects.get_or_create(username="u1")
        bookmarks = get_bookmarks_for(u1.username)
        
        self.assertTrue(ob.has_perm(u1, "menus.view_menu", bookmarks))
        self.assertTrue(ob.has_perm(u1, "menus.change_menu", bookmarks))
        self.assertTrue(ob.has_perm(u1, "menus.delete_menu", bookmarks))        
        
    def test_manage_author_permissions_on_bookmark(self):
        """Tests that "manage_author_permissions" auto-generate perms for author. 
        """
        user_model = get_user_model()
        
        u2, n = user_model.objects.get_or_create(username="u2")
        u3, n = user_model.objects.get_or_create(username="u3")
        
        prev_user = logged_cache.user
        
        # The current author ("logged" user) is now u2.
        logged_cache.user = u2
        
        b1, n = Bookmark.objects.get_or_create(menu=get_bookmarks_for(u2.username), title="b1", url="/")
        
        self.assertTrue(ob.has_perm(u2, "menus.view_link", b1))
        self.assertTrue(ob.has_perm(u2, "menus.change_link", b1))
        self.assertTrue(ob.has_perm(u2, "menus.delete_link", b1))
        
        self.assertFalse(ob.has_perm(u3, "menus.view_link", b1))
        self.assertFalse(ob.has_perm(u3, "menus.change_link", b1))
        self.assertFalse(ob.has_perm(u3, "menus.delete_link", b1))
        
        # Restores previous cached user.
        logged_cache.user = prev_user
        
    def test_bookmarks_auto_deletion(self):
        """Tests automatic deletion of bookmarks when their owners are deleted.
        """
        d = None
        
        try:
            d = get_bookmarks_for("u4")
        except:
            pass
            
        self.assertEqual(d, None)
            
        u4, n = get_user_model().objects.get_or_create(username="u4")
        
        try:
            d = get_bookmarks_for("u4")
        except:
            pass
            
        self.assertNotEqual(d, None)
        
        u4.delete()
        
        try:
            d = get_bookmarks_for("u4")
        except:
            d = None
            
        self.assertEqual(d, None)
