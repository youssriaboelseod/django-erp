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

from ..models import Region, Plugget

class RegionTestCase(TestCase):
    def setUp(self):
        from django.contrib.contenttypes.models import ContentType
        
        user_model = get_user_model()
        
        self.u1 = user_model.objects.create(username="u1")
        self.r1 = Region.objects.create(slug="r1")
        self.r2 = Region.objects.create(
            slug="r2",
            title="Region 2",
            content_type=ContentType.objects.get_for_model(user_model),
            object_id=self.u1.pk
        )
        
    def test_get_absolute_url_without_owner(self):
        """Tests the "get_absolute_url" method of a region without owner object.
        """
        self.assertEqual(self.r1.get_absolute_url(), "/")
        
    def test_get_absolute_url_with_user_as_owner(self):
        """Tests the "get_absolute_url" method of a region with an owner object.
        """
        self.assertNotEqual(self.r2.get_absolute_url(), self.u1.get_absolute_url())
        self.assertEqual(self.r2.get_absolute_url(), "/")
        
    def test_get_absolute_url_with_owner(self):
        """Tests the "get_absolute_url" method of a region with an owner object.
        """
        # TODO: use a custom model as owner of a region.
        pass
        
    def test_unicode(self):
        """Tests getting correct unicode representation.
        """
        self.assertEqual("%s" % self.r1, "r1")
        self.assertEqual("%s" % self.r2, "Region 2")

class PluggetTestCase(TestCase):
    def setUp(self):
        self.r1 = Region.objects.create(slug="r1", title="Region 1")
        self.p1 = Plugget.objects.create(region=self.r1, title="Plugget 1", source="djangoerp.pluggets.base.dummy", template="pluggets/base_plugget.html")
        
    def test_get_absolute_url(self):
        """Tests the "get_absolute_url" method of a plugget.
        """
        self.assertEqual(self.p1.get_absolute_url(), self.r1.get_absolute_url())
        
    def test_unicode(self):
        """Tests getting correct unicode representation.
        """
        self.assertEqual("%s" % self.p1, "%s | %s" % (self.r1, self.p1.title))
        
    def test_slug_func(self):
        """Tests getting Plugget slug.
        """
        self.assertEqual(self.p1.slug(), "region-1_plugget-1")
        
    def test_get_edit_url(self):
        """Tests retrieving the Plugget's URL for editing.
        """
        self.assertEqual(self.p1.get_edit_url(), "/pluggets/%d/edit/" % self.p1.pk)
        
    def test_get_delete_url(self):
        """Tests retrieving the Plugget's URL for deletion.
        """
        self.assertEqual(self.p1.get_delete_url(), "/pluggets/%d/delete/" % self.p1.pk)
