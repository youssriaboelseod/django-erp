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
from django.shortcuts import resolve_url
from django.contrib.auth import get_user_model

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
        
class DeletePluggetViewTestCase(TestCase):
    def setUp(self):
        from djangoerp.core.models import ObjectPermission
        
        user_model = get_user_model()
               
        self.u1 = user_model.objects.create_user("u1", "u@u.it", "password")
        self.u2 = user_model.objects.create_user("u2", "u@u.it", "password")
        self.u3 = user_model.objects.create_user("u3", "u@u.it", "password")
        self.u4 = user_model.objects.create_user("u4", "u@u.it", "password")
        self.r = Region.objects.create(slug="r")
        self.p = Plugget.objects.create(title="Plugget", source="", region=self.r)
        
        rp, n = ObjectPermission.objects.get_or_create_by_uid("pluggets.change_region.%d" % self.r.pk)
        pp, n = ObjectPermission.objects.get_or_create_by_uid("pluggets.delete_plugget.%d" % self.p.pk)
        
        self.u2.objectpermissions.add(rp)
        self.u3.objectpermissions.add(pp)
        self.u4.objectpermissions.add(rp)
        self.u4.objectpermissions.add(pp)
        
        self.url = resolve_url("plugget_delete", pk=self.p.pk)
        
    def test_deny_anonymous_user(self):
        """Tests anonymous users can not access the view.
        """
        self.client.logout()
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 302)
        
    def test_logged_user_without_perms(self):
        """Tests deny access to users without correct perms.
        """        
        self.client.login(username='u1', password='password')
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 302)
        
    def test_logged_user_with_partial_perms(self):
        """Tests deny access to users without correct perms.
        """        
        self.client.login(username='u2', password='password')
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 302)
        
        self.client.login(username='u3', password='password')
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 302)
        
    def test_logged_user_with_perms(self):
        """Tests logged users with correct perms can access the view.
        """        
        self.client.login(username='u4', password='password')
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        
    def test_set_urls_in_get_object(self):
        """Tests correct setting of next/back URLs in "get_object" method.
        """
        v = DeletePluggetView()
        v.kwargs = {"pk": self.p.pk}
        
        p = v.get_object()
        
        self.assertEqual(p, self.p)
        self.assertEqual(v.cancel_url, self.r.get_absolute_url())
        self.assertEqual(v.success_url, self.r.get_absolute_url())
