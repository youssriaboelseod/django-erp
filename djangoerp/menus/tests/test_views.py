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
from django.shortcuts import resolve_url
from django.contrib.auth import get_user_model

from . import *
from ..views import *
from ..views import _get_bookmarks, _get_bookmark # NOTE: not in public API!
        
class _FakeBaseView(object):
    def __init__(self, *args, **kwargs):
        self.request = FakeRequest()
        self.request.user, n = get_user_model().objects.get_or_create(username="u")
        self.args = args
        self.kwargs = kwargs
        
    def get_form_kwargs(self):
        return {}
        
    def get_initial(self):
        return {}
        
    def get_queryset(self):
        return Bookmark.objects.all()    

class GetterFunctionsTestCase(TestCase):
    def setUp(self):
        self.request = FakeRequest()
        self.request.user, n = get_user_model().objects.get_or_create(username="u")
        self.user_bookmarks = Menu.objects.get(slug="user_1_bookmarks")
        self.user_bookmark = Bookmark.objects.create(title="Bookmark", slug="bookmark", url="/", menu=self.user_bookmarks)
        
    def test_get_bookmarks(self):
        """Tests _get_bookmarks getter function.
        """
        self.assertEqual(_get_bookmarks(self.request), self.user_bookmarks)
        
    def test_get_bookmark(self):
        """Tests _get_bookmark getter function.
        """
        self.assertEqual(_get_bookmark(self.request, slug="bookmark"), self.user_bookmark)
        
class BookmarkMixinTestCase(TestCase):
    def setUp(self):                
        class TestBookmarkMixin(BookmarkMixin, _FakeBaseView):
            pass
            
        self.m = TestBookmarkMixin()
        self.user_bookmarks = Menu.objects.get(slug="user_1_bookmarks")
        self.user_bookmark1 = Bookmark.objects.create(title="Bookmark 1", slug="bookmark1", url="/", menu=self.user_bookmarks)
        self.user_bookmark2 = Bookmark.objects.create(title="Bookmark 2", slug="bookmark2", url="/", menu=self.user_bookmarks)
        
    def test_get_queryset(self):
        """Tests "BookmarkMixin.get_queryset" method.
        """
        self.assertEqual(self.m.get_queryset().count(), 2)
        self.assertQuerysetEqual(
            self.m.get_queryset(),
            [
                repr(self.user_bookmark1),
                repr(self.user_bookmark2)
            ],
            ordered=False
        )          
    
class BookmarkCreateUpdateMixinTestCase(TestCase):
    def setUp(self):                
        class TestBookmarkCreateUpdateView(BookmarkCreateUpdateMixin, _FakeBaseView):
            pass
            
        self.v = TestBookmarkCreateUpdateView()
        self.user_bookmarks = Menu.objects.get(slug="user_1_bookmarks")
        
    def test_get_form_kwargs(self):
        """Tests "BookmarkCreateUpdateMixin.get_form_kwargs" method.
        """
        kwargs = self.v.get_form_kwargs()
        self.assertTrue("menu" in kwargs)
        self.assertEqual(kwargs['menu'], self.user_bookmarks)
        
    def test_get_initial_url_on_creation(self):
        """Tests the initial URL is set on the current path on bookmark creation.
        """
        self.v.object = None
        self.assertEqual(self.v.get_initial(), {"url": "/bookmarks/"})
        
    def test_get_initial_url_on_editing(self):
        """Tests the initial URL is not set on bookmark editing.
        """
        self.v.object = Bookmark()
        self.assertEqual(self.v.get_initial(), {})

class ListBookmarkViewTestCase(TestCase):        
    def test_deny_anonymous_user(self):
        """Tests anonymous users can not access the view.
        """
        self.client.logout()
        response = self.client.get(resolve_url("bookmark_list"))
        
        self.assertEqual(response.status_code, 302)
        
    def test_logged_user_with_perms(self):
        """Tests logged users with correct perms can access the view.
        """
        u = get_user_model().objects.create_user("u", "u@u.it", "password")
        
        self.client.login(username='u', password='password')
        response = self.client.get(resolve_url("bookmark_list"))
        
        self.assertEqual(response.status_code, 200)

class CreateBookmarkViewTestCase(TestCase):        
    def test_deny_anonymous_user(self):
        """Tests anonymous users can not access the view.
        """
        self.client.logout()
        response = self.client.get(resolve_url("bookmark_add"))
        
        self.assertEqual(response.status_code, 302)
        
    def test_logged_user_without_perms(self):
        """Tests logged users without correct perms can not access the view.
        """
        from djangoerp.core.models import User, Group

        u1 = User.objects.create_user("u1", "u@u.it", "password")

        # Permission to add bookmarks is given by default "users" Group.
        u1.groups.remove(Group.objects.get(name="users"))
        
        self.client.login(username='u1', password='password')
        response = self.client.get(resolve_url("bookmark_add"))
        
        self.assertEqual(response.status_code, 302)
        
    def test_logged_user_with_perms(self):
        """Tests logged users with correct perms can access the view.
        """
        from djangoerp.core.models import Permission

        u2 = get_user_model().objects.create_user("u2", "u@u.it", "password")
        p, n = Permission.objects.get_or_create_by_uid("menus.add_link")

        u2.user_permissions.add(p)
        
        self.client.login(username='u2', password='password')
        response = self.client.get(resolve_url("bookmark_add"))
        
        self.assertEqual(response.status_code, 200)

class UpdateBookmarkViewTestCase(TestCase):
    def setUp(self):
        from ..utils import get_bookmarks_for
        
        self.u1 = get_user_model().objects.create_user("u1", "u@u.it", "password")
        self.u2 = get_user_model().objects.create_user("u2", "u@u.it", "password")
        self.b = Bookmark.objects.create(title="Bookmark", slug="bookmark", url="/", menu=get_bookmarks_for(self.u2))
        
    def test_deny_anonymous_user(self):
        """Tests anonymous users can not access the view.
        """
        self.client.logout()
        response = self.client.get(resolve_url("bookmark_edit", slug=self.b.slug))
        
        self.assertEqual(response.status_code, 302)
        
    def test_not_owner_user(self):
        """Tests deny access to other user's bookmarks.
        """        
        self.client.login(username='u1', password='password')
        response = self.client.get(resolve_url("bookmark_edit", slug=self.b.slug))
        
        self.assertEqual(response.status_code, 404)
        
    def test_logged_user_with_perms(self):
        """Tests logged users with correct perms can access the view.
        """
        from djangoerp.core.models import Permission
        
        p, n = Permission.objects.get_or_create_by_uid("menus.change_link")
        self.u2.user_permissions.add(p)
        
        self.client.login(username='u2', password='password')
        response = self.client.get(resolve_url("bookmark_edit", slug=self.b.slug))
        
        self.assertEqual(response.status_code, 200)

class DeleteBookmarkViewTestCase(TestCase):
    def setUp(self):
        from ..utils import get_bookmarks_for
        
        self.u1 = get_user_model().objects.create_user("u1", "u@u.it", "password")
        self.u2 = get_user_model().objects.create_user("u2", "u@u.it", "password")
        self.b = Bookmark.objects.create(title="Bookmark", slug="bookmark", url="/", menu=get_bookmarks_for(self.u2))
        
    def test_deny_anonymous_user(self):
        """Tests anonymous users can not access the view.
        """
        self.client.logout()
        response = self.client.get(resolve_url("bookmark_delete", slug=self.b.slug))
        
        self.assertEqual(response.status_code, 302)
        
    def test_not_owner_user(self):
        """Tests deny access to other user's bookmarks.
        """        
        self.client.login(username='u1', password='password')
        response = self.client.get(resolve_url("bookmark_delete", slug=self.b.slug))
        
        self.assertEqual(response.status_code, 404)
        
    def test_logged_user_with_perms(self):
        """Tests logged users with correct perms can access the view.
        """
        from djangoerp.core.models import Permission
        
        p, n = Permission.objects.get_or_create_by_uid("menus.delete_link")
        self.u2.user_permissions.add(p)
        
        self.client.login(username='u2', password='password')
        response = self.client.get(resolve_url("bookmark_delete", slug=self.b.slug))
        
        self.assertEqual(response.status_code, 200)
