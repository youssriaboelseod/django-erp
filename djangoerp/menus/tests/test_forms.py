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
from django.forms import ValidationError

from . import *
from ..models import *
from ..forms import *
    
class BookmarkFormTestCase(TestCase):
    def setUp(self):
        self.m, n = Menu.objects.get_or_create(slug="test-bookmarks")
        
    def test_clean_title(self):
        """Tests cleaning title field.
        """
        data = {"title": "Test Bookmark", "slug": "bookmark1", "url": "/"}
        
        f = BookmarkForm(data, menu=self.m)
        
        self.assertTrue(f.is_valid())
        
        b1 = f.save()
        
        self.assertTrue(isinstance(b1, Bookmark))
        
        f = BookmarkForm(data, instance=b1)
        
        self.assertTrue(f.is_valid())
        self.assertEqual(f.save(), b1)
        
        f = BookmarkForm(data, menu=self.m)
        
        self.assertFalse(f.is_valid())
        #self.assertRaises(ValidationError, f.clean_title)
        self.assertTrue("This title is already in use." in f.errors.get("title", []))
        
    def test_fail_on_no_menu(self):
        """Tests failing when no menu is specified.
        """
        data = {"title": "Test Bookmark", "slug": "bookmark1", "url": "/"}
        
        f = BookmarkForm(data)
        
        self.assertRaises(Menu.DoesNotExist, f.save)
        
        b = Bookmark()
        f = BookmarkForm(data, instance=b)
        
        self.assertRaises(Menu.DoesNotExist, f.save)
