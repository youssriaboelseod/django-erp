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

from ..models import Region, Plugget
from ..loading import registry
from ..forms import *

class SelectPluggetSourceFormTestCase(TestCase):
    def test_populate_source_choices(self):
        """Tests correct populating of source choices.
        """
        registry.clear()
        registry.discovered = True
        
        source_title1 = "Source 1"
        source_title2 = "Source 2"
        
        registry.register_simple_plugget_source(source_title1)
        registry.register_simple_plugget_source(source_title2)
        
        f = SelectPluggetSourceForm()
        choices = f.fields['source_uid'].choices
        
        self.assertEqual(len(choices), 2)
        self.assertTrue((source_title1, source_title1) in choices)
        self.assertTrue((source_title2, source_title2) in choices)
        
class CustomizePluggetSettingsFormTestCase(TestCase):
    def setUp(self):
        self.r = Region.objects.create(slug="r")
        self.p = Plugget.objects.create(title="Plugget", source="", region=self.r)
        
    def test_set_region(self):
        """Tests correct setting of region attribute via "region" kwarg.
        """
        f = CustomizePluggetSettingsForm()
        
        self.assertEqual(f.region, None)
        
        f = CustomizePluggetSettingsForm(region="My Region")
        
        self.assertEqual(f.region, "My Region")
        
    def test_clean_title_when_title_is_new(self):
        """Tests correct validation of title field when its value is a new one.
        """
        f = CustomizePluggetSettingsForm({"title": "A new plugget"}, region=self.r)
        
        self.assertTrue(f.is_valid())
        
    def test_raise_error_when_title_already_exists(self):
        """Tests correct validation of title field when its value is already used.
        """
        f = CustomizePluggetSettingsForm({"title": "Plugget"}, region=self.r)
        
        self.assertFalse(f.is_valid())
        #self.assertRaises(ValidationError, f.clean_title)
        self.assertTrue("This title is already in use." in f.errors.get("title", []))
        
    def test_correct_title_validation_on_plugget_editing(self):
        """Tests correct validation of title field on plugget editing. 
        """
        f = CustomizePluggetSettingsForm({"title": "Plugget"}, instance=self.p)
        
        self.assertTrue(f.is_valid())
