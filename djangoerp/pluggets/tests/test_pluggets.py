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
from django.template import Context
from django.contrib.auth import get_user_model
from djangoerp.menus.models import Menu

class MenuPluggetFuncTestCase(TestCase):
    def test_with_menu_id(self):
        """Tests context manipulation when "menu_id" is in the given context.
        """
        # WARNING: Don't put this line at module level due to issues with
        #          plugget auto-discovering.
        from ..pluggets import menu

        m = Menu.objects.create(slug="test-menu")
        
        context = menu(Context({"menu_id": m.pk}))
        
        self.assertTrue("menu_id" not in context)
        self.assertTrue("name" in context)
        self.assertEqual(context['name'], "test-menu")
        
    def test_without_menu_id(self):
        """Tests context manipulation when "menu_id" is not in the given context.
        """
        # WARNING: Don't put this line at module level due to issues with
        #          plugget auto-discovering.
        from ..pluggets import menu
        
        context = menu(Context())
        
        self.assertTrue("menu_id" not in context)
        self.assertTrue("name" not in context)

class BookmarksMenuPluggetFuncTestCase(TestCase):
    def test_with_user(self):
        """Tests context manipulation when "user" is in the given context.
        """
        # WARNING: Don't put this line at module level due to issues with
        #          plugget auto-discovering.
        from ..pluggets import bookmarks_menu
        
        u = get_user_model().objects.create(username="u", password="p")
        
        context = bookmarks_menu(Context({"user": u}))
        
        self.assertTrue("menu_id" not in context)
        self.assertTrue("name" in context)
        self.assertEqual(context['name'], "user_%d_bookmarks" % u.pk)
        
    def test_without_user(self):
        """Tests context manipulation when "user" is not in the given context.
        """
        # WARNING: Don't put this line at module level due to issues with
        #          plugget auto-discovering.
        from ..pluggets import bookmarks_menu
        
        context = bookmarks_menu(Context())
        
        self.assertTrue("menu_id" not in context)
        self.assertTrue("name" not in context)
