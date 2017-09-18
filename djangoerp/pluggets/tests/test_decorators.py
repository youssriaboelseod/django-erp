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
from django.shortcuts import render_to_response

from ..models import Region, Plugget
from ..loading import registry
from ..decorators import *

class PseudoResponse:
    pass

class IsPluggetEditableDecoratorTestCase(TestCase):
    def setUp(self):
        source_title = "Editable plugget"
        registry.register_simple_plugget_source(source_title)
        
        self.r = Region.objects.create(slug="r")
        self.pluggets = (
            # Editable plugget.
            Plugget.objects.create(region=self.r, title="Editable", source=source_title),
            # Not-editable plugget.
            Plugget.objects.create(region=self.r, title="Not editable", source="djangoerp.pluggets.loading.plugget_source_registry.default_func")
        )

        @is_plugget_editable(lambda x : self.pluggets[x])        
        def test_decorator_view(request, *args, **kwargs):
            return PseudoResponse()
            
        self.v = test_decorator_view
        
    def test_with_editable_plugget(self):
        """Tests allowing access to the view when an editable plugget is used.
        """
        response = self.v(0)
        
        self.assertTrue(isinstance(response, PseudoResponse))
        
    def test_with_not_editable_plugget(self):
        """Tests denying access to the view when a not editable plugget is used.
        """
        response = self.v(1)
        
        self.assertFalse(isinstance(response, PseudoResponse))
