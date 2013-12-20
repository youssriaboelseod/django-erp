#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
__copyright__ = 'Copyright (c) 2013 Emanuele Bertoldi'
__version__ = '0.0.3'

from django.test import TestCase
from django.contrib.auth import get_user_model

from . import *
from ..views import *
from ..views import _get_bookmarks, _get_bookmark # NOTE: not in public API!

class GetterFunctionsTestCase(TestCase):
    def setUp(self):
        self.u, n = get_user_model().objects.get_or_create(username="u")
        self.request = FakeRequest()
        self.request.user = self.u
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
    
class BookmarkCreateUpdateMixinTestCase(TestCase):
    def setUp(self):
        class _FakeBaseView(object):
            def get_initial(self):
                return {}
                
        class FakeBookmarkCreateUpdateView(BookmarkCreateUpdateMixin, _FakeBaseView):
            pass
            
        self.v = FakeBookmarkCreateUpdateView()
        
    def test_get_initial_url_on_creation(self):
        """Tests the initial URL is set on the current path on bookmark creation.
        """
        self.v.request = FakeRequest()
        self.v.object = None
        self.assertEqual(self.v.get_initial(), {"url": "/bookmarks/"})
        
    def test_get_initial_url_on_editing(self):
        """Tests the initial URL is not set on bookmark editing.
        """
        self.v.request = FakeRequest()
        self.v.object = Bookmark()
        self.assertEqual(self.v.get_initial(), {})
