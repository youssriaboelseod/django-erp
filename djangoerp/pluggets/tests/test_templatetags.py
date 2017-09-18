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
from django.template import Variable, Context
from django.contrib.sites.models import Site

from djangoerp.core.cache import LoggedInUserCache
from ..models import Region, Plugget
from ..templatetags.regions import *
        
def _clean_output(output):
    return "".join([r.strip() for r in output.strip().splitlines() if r and not r.isspace()])

class RenderPluggetTagTestCase(TestCase):
    def setUp(self):
        from ..loading import registry

        LoggedInUserCache().clear()
        
        registry.register_simple_plugget_source("Something")
        
        self.r = Region.objects.create(slug="r")
        self.p1 = Plugget.objects.create(title="Plugget", source="djangoerp.pluggets.pluggets.dummy", context='{"text": "Hi!"}', region=self.r)
        self.p2 = Plugget.objects.create(title="Another Plugget", source="Something", context='{"text": "Hi!"}', region=self.r)
        self.p3 = Plugget.objects.create(title="Invalid Plugget", source="Invalid", context='{"text": "Hi!"}', region=self.r)
        
    def test_with_existing_plugget(self):
        """Tests rendering an existing Plugget instance.
        """
        plugget_pk = Variable("plugget_pk")
        template_name = Variable("template_name")
        context = Context({"plugget_pk": self.p1.pk, "template_name": None})
        
        cleaned_output = _clean_output(render_plugget(context, plugget_pk, template_name))
        
        self.assertEqual(
            cleaned_output,
            '<aside class="plugget r_plugget" id="r_plugget-plugget">'
            '<header>'
            '<h3>Plugget</h3>'
            '<ul class="actions">'
            '</ul>'
            '</header>'
            '<section class="body">'
            'Hi!'
            '</section>'
            '</aside>'
        )
        
    def test_with_registered_plugget_source(self):
        """Tests rendering a Plugget instance with a registered plugget source.
        """        
        cleaned_output = _clean_output(render_plugget(Context(), self.p2.pk))
        
        self.assertEqual(
            cleaned_output,
            '<aside class="plugget r_another-plugget" id="r_another-plugget-plugget">'
            '<header>'
            '<h3>Another Plugget</h3>'
            '<ul class="actions">'
            '</ul>'
            '</header>'
            '<section class="body">'
            'Hi!'
            '</section>'
            '</aside>'
        )
        
    def test_with_invalid_plugget_source(self):
        """Tests rendering a Plugget instance with an invalid plugget source.
        """        
        cleaned_output = _clean_output(render_plugget(Context(), self.p3.pk))
        
        self.assertEqual(
            cleaned_output,
            '<aside class="plugget r_invalid-plugget" id="r_invalid-plugget-plugget">'
            '<header>'
            '<h3>Invalid Plugget</h3>'
            '<ul class="actions">'
            '</ul>'
            '</header>'
            '<section class="body">'
            'Hi!'
            '</section>'
            '</aside>'
        )
        
    def test_with_invalid_plugget(self):
        """Tests invoking the templatetag with an invalid Plugget ID.
        """
        self.assertEqual(render_plugget(Context(), 5454454557576557), "")

class RenderRegionTagTestCase(TestCase):
    def setUp(self):
        LoggedInUserCache().clear()

        self.r = Region.objects.create(slug="r")
        
    def test_with_valid_region(self):
        """Tests invoking the templatetag with a valid Region slug.
        """
        region_slug = Variable("region_slug")
        template_name = Variable("template_name")
        context = Context({"region_slug": self.r.slug, "template_name": None})
        
        cleaned_output = _clean_output(render_region(context, region_slug, template_name))
        
        self.assertEqual(
            cleaned_output,
            '<div class="region" id="r-region"></div>'
        )
        
    def test_with_invalid_region(self):
        """Tests invoking the templatetag with an invalid Region slug.
        """
        self.assertEqual(render_region(Context(), "dashboard"), "")

class RegionsForTagTestCase(TestCase):
    def setUp(self):        
        self.s1 = Site.objects.create(domain="s1", name="s1")
        self.r1 = Region.objects.create(slug="r1", owner_object=self.s1)
        self.r2 = Region.objects.create(slug="r2", owner_object=self.s1)
        
    def test_with_valid_owner(self):
        """Tests invoking the templatetag with a valid owner object.
        """
        self.assertQuerysetEqual(
            regions_for(self.s1),
            [
                repr(self.r1),
                repr(self.r2),
            ],
            ordered=False
        )
        
    def test_with_invalid_owner(self):
        """Tests invoking the templatetag with an invalid owner object.
        """
        self.assertEqual(regions_for(None), [])

class FirstRegionForTagTestCase(TestCase):
    def setUp(self):
        LoggedInUserCache().clear()

        self.s1 = Site.objects.create(domain="s1", name="s1")
        self.r1 = Region.objects.create(slug="r1", owner_object=self.s1)
        self.r2 = Region.objects.create(slug="r2", owner_object=self.s1)
        
    def test_with_valid_owner(self):
        """Tests invoking the templatetag with a valid owner object.
        """
        self.assertEqual(first_region_for(self.s1), self.r1)
        
    def test_with_invalid_owner(self):
        """Tests invoking the templatetag with an invalid owner object.
        """
        self.assertEqual(first_region_for(None), None)
