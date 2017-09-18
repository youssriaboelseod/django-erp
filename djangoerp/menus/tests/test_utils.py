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

from ..models import *
from ..utils import *

class FakeModel():
    pk = 5

class CreateBookmarksUtilTestCase(TestCase):
    def test_create_bookmarks_for_user(self):
        """Tests creating bookmarks for the given user instance.
        """
        u1, n = get_user_model().objects.get_or_create(username="u1")
        m, n = create_bookmarks(u1)
        
        self.assertTrue(isinstance(m, Menu))
        self.assertEqual(m.slug, "user_%d_bookmarks" % u1.pk)
        # NOTE: the bookmark menu was already created by the signal handler.
        self.assertEqual(n, False)
        
    def test_create_bookmarks_for_any_model(self):
        """Tests creating bookmarks for a generic model instance.
        """            
        fm = FakeModel()
        m, n = create_bookmarks(fm)
        
        self.assertTrue(isinstance(m, Menu))
        self.assertEqual(m.slug, "fakemodel_5_bookmarks")
        self.assertEqual(n, True)

class DeleteBookmarksUtilTestCase(TestCase):
    def test_delete_bookmarks_for_user(self):
        """Tests deleting bookmarks of the given user instance.
        """
        u1, n = get_user_model().objects.get_or_create(username="u1")
        m, n = create_bookmarks(u1)
        
        self.assertTrue(isinstance(m, Menu))
        self.assertEqual(
            Menu.objects.filter(slug=get_bookmarks_slug_for(u1)).exists(),
            True
        )
        
        delete_bookmarks(u1)

        self.assertEqual(
            Menu.objects.filter(slug=get_bookmarks_slug_for(u1)).exists(),
            False
        )
        
    def test_delete_bookmarks_for_any_model(self):
        """Tests deleting bookmarks of a generic model instance.
        """            
        fm = FakeModel()
        m, n = create_bookmarks(fm)
        
        self.assertTrue(isinstance(m, Menu))
        self.assertEqual(
            Menu.objects.filter(slug=get_bookmarks_slug_for(fm)).exists(),
            True
        )
        
        delete_bookmarks(fm)

        self.assertEqual(
            Menu.objects.filter(slug=get_bookmarks_slug_for(fm)).exists(),
            False
        )
        
    def test_delete_bookmarks_without_bookmarks(self):
        """Tests calling "delete_bookmarks" on an instance without bookmarks.
        """           
        fm = FakeModel()
        
        self.assertEqual(
            Menu.objects.filter(slug=get_bookmarks_slug_for(fm)).exists(),
            False
        )
        
        delete_bookmarks(fm)
        
        self.assertEqual(
            Menu.objects.filter(slug=get_bookmarks_slug_for(fm)).exists(),
            False
        )
        
class GetBookmarksForUtilTestCase(TestCase):
    def test_bookmarks_for_user(self):
        """Tests retrieving bookmark list owned by user with a given username.
        """        
        u1, n = get_user_model().objects.get_or_create(username="u1")
        
        self.assertTrue(n)
        
        bookmarks = Menu.objects.get(slug=get_bookmarks_slug_for(u1))
        
        self.assertEqual(get_bookmarks_for(u1.username), bookmarks)
       
class GetUserOfUtilTestCase(TestCase):        
    def test_user_of_bookmarks(self):
        """Tests retrieving the user of bookmarks identified by the given slug.
        """        
        u1, n = get_user_model().objects.get_or_create(username="u1")
        bookmarks = Menu.objects.get(slug="user_1_bookmarks")
        
        self.assertEqual(get_user_of(bookmarks.slug), u1)
        
class CreateDetailNavigationTestCase(TestCase):
    def test_create_detail_navigation(self):
        """Tests creating a detail view navigation menu.
        """
        m, n = create_detail_navigation(FakeModel)
        
        self.assertEqual(m.slug, "fakemodel_detail_navigation")
        self.assertEqual(m.description, "Fakemodel navigation")
        
class CreateDetailActionsTestCase(TestCase):
    def test_create_detail_actions(self):
        """Tests creating a detail view action menu.
        """
        m, n = create_detail_actions(FakeModel)
        
        self.assertEqual(m.slug, "fakemodel_detail_actions")
        self.assertEqual(m.description, "Fakemodel actions")
        
class CreateListActionsTestCase(TestCase):
    def test_create_list_actions(self):
        """Tests creating a list view action menu.
        """
        m, n = create_list_actions(FakeModel)
        
        self.assertEqual(m.slug, "fakemodel_list_actions")
        self.assertEqual(m.description, "Fakemodel list actions")
