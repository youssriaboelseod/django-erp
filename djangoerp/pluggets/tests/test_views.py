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
__version__ = '0.0.4'

from django.test import TestCase

from ..models import Region, Plugget
from ..views import *
from ..views import _get_plugget, _get_plugget_add_or_edit_perm, _get_region # NOTE: not in public API!

class GetterFunctionsTestCase(TestCase):
    def setUp(self):
        self.r = Region.objects.create(slug="r")
        self.p = Plugget.objects.create(title="Plugget", source="", region=self.r)
        
    def test_get_plugget_with_pk_kwarg(self):
        """Tests _get_plugget getter when a "pk" kwarg is provided.
        """
        self.assertEqual(_get_plugget(pk=self.p.pk), self.p)
        
    def test_get_plugget_without_pk_kwarg(self):
        """Tests _get_plugget getter when no "pk" kwarg is provided.
        """
        self.assertEqual(_get_plugget(), None)
        
    def test_get_plugget_add_or_edit_perm_with_pk_kwarg(self):
        """Tests _get_plugget_add_or_edit_permr func when a "pk" kwarg is provided.
        """
        self.assertEqual(_get_plugget_add_or_edit_perm(pk=self.p.pk), "pluggets.change_plugget")
        
    def test_get_plugget_add_or_edit_perm_without_pk_kwarg(self):
        """Tests _get_plugget_add_or_edit_permr func when no "pk" kwarg is provided.
        """
        self.assertEqual(_get_plugget_add_or_edit_perm(), "pluggets.add_plugget")
        
    def test_get_region_with_slug_kwarg(self):
        """Tests _get_region getter when a "slug" kwarg is provided.
        """
        self.assertEqual(_get_region(slug=self.r.slug), self.r)
        
    def test_get_region_with_pk_but_without_slug_kwarg(self):
        """Tests _get_region function when "pk" kwarg is provided but "slug" no.
        """
        self.assertEqual(_get_region(pk=self.p.pk), self.r)
        
    def test_get_region_without_pk_and_slug_kwarg(self):
        """Tests _get_region function when "pk" nor "slug" kwargs are provided.
        """
        self.assertRaises(Region.DoesNotExist, _get_region)
