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

from ..models import *
    
class MenuTestCase(TestCase):
    def test_unicode_representation(self):
        """Tests Menu's unicode representation.
        """
        m = Menu.objects.create(slug="menu")
        
        self.assertEqual(u"%s" % m, "menu")
        
        m.description = "A test menu."
        
        self.assertEqual(u"%s" % m, "A test menu.")
    
class LinkTestCase(TestCase):
    urls = 'djangoerp.menus.tests.urls'
    
    def setUp(self):
        self.m = Menu.objects.create(slug="menu")
        
    def test_unicode_representation(self):
        """Tests Link's unicode representation.
        """
        l, n = Link.objects.get_or_create(title="Test Link", slug="l", url="/", menu=self.m)
        
        self.assertEqual(u"%s" % l, "menu | Test Link")
        
    def test_plain_absolute_url(self):
        """Tests retrieving a plain Link's absolute URL.
        """
        l1, n = Link.objects.get_or_create(title="Test Link 1", slug="l1", url="/", menu=self.m)
        
        self.assertEqual(l1.get_absolute_url(), "/")
        
    def test_reversing_absolute_url(self):
        """Tests reversing the Link's absolute URL.
        """
        l2, n = Link.objects.get_or_create(title="Test Link 2", slug="l2", url="private_zone_url", context='{"id": "link_url_id_kwarg"}', menu=self.m)
        l2.extra_context = {
            "link_url_id_kwarg": "1",
        }
        
        self.assertEqual(l2.get_absolute_url(), "/private/1")
        
    def test_invalid_absolute_url_reversion(self):
        """Tests invalid Link's absolute URL reversion.
        """
        # NOTE: "private_url" is an invalid URL's name, so there's no valid reversion.
        l3, n = Link.objects.get_or_create(title="Test Link 3", slug="l3", url="private_url", menu=self.m)
        
        self.assertEqual(l3.get_absolute_url(), "private_url")
