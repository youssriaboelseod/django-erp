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

from django.test import TestCase, RequestFactory
from django.shortcuts import resolve_url
from django.contrib.auth import get_user_model
from djangoerp.core.models import Permission, ObjectPermission

from ..loading import registry
from ..models import Region, Plugget
from ..views import *
from ..views import _get_plugget, _get_plugget_add_or_edit_perm, _get_region # NOTE: not in public API!

class FakeStorage(object):
    extra_data = {}
    data = {}
    
    def get_step_data(self, step=None):
        return self.data.get(step, {})
        
class FakeSteps(list):
    current = '0'

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
        
class PluggetWizardTestCase(TestCase):
    def setUp(self):
        from django import forms
        
        self.factory = RequestFactory()
        
        user_model = get_user_model()
        
        class TestForm(forms.Form):
            text = forms.CharField(initial="Something...", required=True, widget=forms.Textarea)
            user = forms.ModelChoiceField(queryset=user_model.objects.all())

        registry.register_simple_plugget_source("Test", description="A test plugget source", form=TestForm)
               
        self.u1 = user_model.objects.create_user("u1", "u@u.it", "password")
        self.u2 = user_model.objects.create_user("u2", "u@u.it", "password")
        self.u3 = user_model.objects.create_user("u3", "u@u.it", "password")
        self.r = Region.objects.create(slug="r")
        self.p = Plugget.objects.create(title="Plugget", source="Test", context='{"text": "My plugget text", "user": 1}', region=self.r)
        
        rp, n = ObjectPermission.objects.get_or_create_by_uid("pluggets.change_region.%d" % self.r.pk)
        pp, n = ObjectPermission.objects.get_or_create_by_uid("pluggets.change_plugget.%d" % self.p.pk)
        ap, n = Permission.objects.get_or_create_by_uid("pluggets.add_plugget")
        
        self.u2.objectpermissions.add(rp)
        self.u2.user_permissions.add(ap)
        self.u3.objectpermissions.add(rp)
        self.u3.objectpermissions.add(pp)
        
        self.add_url = resolve_url("plugget_add", slug=self.r.slug)
        self.edit_url = resolve_url("plugget_edit", pk=self.p.pk)
        
    def test_deny_anonymous_user(self):
        """Tests anonymous users can not access the view.
        """
        self.client.logout()
        response = self.client.get(self.add_url)
        
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get(self.edit_url)
        
        self.assertEqual(response.status_code, 302)
        
    def test_logged_user_without_perms(self):
        """Tests deny access to users without correct perms.
        """        
        self.client.login(username='u1', password='password')
        response = self.client.get(self.add_url)
        
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get(self.edit_url)
        
        self.assertEqual(response.status_code, 302)
        
    def test_logged_user_with_perms_to_add_new_plugget(self):
        """Tests logged users with correct perms can access the "add" view.
        """        
        self.client.login(username='u2', password='password')
        response = self.client.get(self.add_url)
        
        self.assertEqual(response.status_code, 200)
        
    def test_logged_user_with_perms_to_edit_plugget(self):
        """Tests logged users with correct perms can access the "edit" view.
        """        
        self.client.login(username='u3', password='password')
        response = self.client.get(self.edit_url)
        
        self.assertEqual(response.status_code, 200)
        
    def test_get_form_kwargs_on_adding(self):
        """Tests "get_form_kwargs" method on plugget adding.
        """
        v = PluggetWizard()
        v.kwargs = {"slug": self.r.slug}
        
        form_kwargs = v.get_form_kwargs("0")
        
        self.assertEqual(form_kwargs, {})
        self.assertEqual(v.region, self.r)
        
        form_kwargs = v.get_form_kwargs("1")
        
        self.assertEqual(form_kwargs, {"region": self.r})
        self.assertEqual(v.region, self.r)
        
    def test_get_form_kwargs_on_editing(self):
        """Tests "get_form_kwargs" method on plugget editing.
        """
        v = PluggetWizard()
        v.kwargs = {"pk": self.p.pk}
        
        form_kwargs = v.get_form_kwargs("0")
        
        self.assertEqual(form_kwargs, {})
        self.assertEqual(v.instance, self.p)
        self.assertEqual(v.region, self.r)
        
        form_kwargs = v.get_form_kwargs("1")
        
        self.assertEqual(form_kwargs, {"region": self.r})
        self.assertEqual(v.instance, self.p)
        self.assertEqual(v.region, self.r)
        
    def test_get_form(self):
        """Tests "get_form" method.
        """
        from django import forms
                
        v = PluggetWizard()
        v.storage = FakeStorage()
        v.initial_dict = {}
        v.kwargs = {"pk": self.p.pk}
        v.form_list = {
            '0': PluggetWizard.DEFAULT_FORMS[0],
            '1': PluggetWizard.DEFAULT_FORMS[1],
        }
        v.source = registry.get_plugget_source(self.p.source)
        
        f = v.get_form('1')
        
        self.assertTrue("text" in f.fields)
        self.assertTrue(isinstance(f.fields['text'], forms.CharField))
        
    def test_get_form_instance(self):
        """Tests "get_form_instance" method.
        """
        v = PluggetWizard(instance=self.p)
        v.instance_dict = {
            '0': "instance0",
            '1': "instance1",
        }
        
        self.assertEqual(v.get_form_instance('0'), "instance0")
        self.assertEqual(v.get_form_instance('1'), self.p)
        self.assertEqual(v.get_form_instance('2'), None)
        
    def test_get_form_initial(self):
        """Tests "get_form_initial" method.
        """
        class NoFinishedStepStorage(FakeStorage):
            pass
                
        class FirstStepFinishedStorage(FakeStorage):
            data = {'0': {'0-source_uid': "Test"}}
                
        class AllStepFinishedStorage(FakeStorage):
            data = {
                '0': {'0-source_uid': "Test"},
                '1': {'1-title': "My Title", '1-text': "A text paragraph.", "1-user": 1}
            }
                
        v = PluggetWizard(region=self.r)
        v.initial_dict = {}
        v.storage = NoFinishedStepStorage()
        
        self.assertEqual(
            v.get_form_initial('0'),
            {
                "region_slug": self.r.slug,
                "source_uid": None,
            }
        )
        
        v.storage = FirstStepFinishedStorage()
        
        self.assertEqual(
            v.get_form_initial('0'),
            {
                "region_slug": self.r.slug,
                "source_uid": "Test",
            }
        )
        
        self.assertEqual(
            v.get_form_initial('1'),
            {
                "title": "Test",
            }
        )
        
        v.storage = AllStepFinishedStorage()
        
        self.assertEqual(
            v.get_form_initial('0'),
            {
                "region_slug": self.r.slug,
                "source_uid": "Test",
            }
        )
        
        self.assertEqual(
            v.get_form_initial('1'),
            {
                "title": "My Title",
            }
        )
        
        v.instance = self.p
        v.storage = NoFinishedStepStorage()
        
        self.assertEqual(
            v.get_form_initial('0'),
            {
                "region_slug": self.r.slug,
                "source_uid": "Test",
            }
        )
        
        v.storage = FirstStepFinishedStorage()
        
        self.assertEqual(
            v.get_form_initial('0'),
            {
                "region_slug": self.r.slug,
                "source_uid": "Test",
            }
        )
        
        self.assertEqual(
            v.get_form_initial('1'),
            {
                "title": "Plugget",
                "text": "My plugget text",
                "user": 1,
            }
        )
        
        v.storage = AllStepFinishedStorage()
        
        self.assertEqual(
            v.get_form_initial('0'),
            {
                "region_slug": self.r.slug,
                "source_uid": "Test",
            }
        )
        
        self.assertEqual(
            v.get_form_initial('1'),
            {
                "title": "My Title",
                "text": "My plugget text",
                "user": 1,
            }
        )
        
    def test_set_cancel_url(self):
        """Tests settng correct "cancel_url".
        """                
        v = PluggetWizard(region=self.r)
        v.initial_dict = {}
        v.storage = FakeStorage()
        
        v.get_form_initial('0') # Here "cancel_url" should be set.
        
        self.assertEqual(v.cancel_url, self.r.get_absolute_url())
        
    def test_get_context_data(self):
        """Tests "get_context_data" method.
        """        
        v = PluggetWizard(region=self.r)
        v.storage = FakeStorage()
        v.steps = FakeSteps()
        v.request = self.factory.get(self.add_url)
        v.prefix = ""
        
        context = v.get_context_data(None)
        
        self.assertTrue("region" in context)
        self.assertEqual(context['region'], self.r)
        self.assertTrue("object" in context)
        self.assertEqual(context['object'], None)
        
        v.instance = self.p
        v.request = self.factory.get(self.edit_url)
        
        context = v.get_context_data(None)
        
        self.assertTrue("region" in context)
        self.assertEqual(context['region'], self.r)
        self.assertTrue("object" in context)
        self.assertEqual(context['object'], self.p)    
        
        v.steps.current = '1'
        v.source = registry.get_plugget_source(self.p.source)
        
        context = v.get_context_data(None)
        
        self.assertTrue("region" in context)
        self.assertEqual(context['region'], self.r)
        self.assertTrue("object" in context)
        self.assertEqual(context['object'], self.p)
        self.assertTrue("plugget_description" in context)
        self.assertEqual(context['plugget_description'], "A test plugget source")
  
    def test_wizard_done(self):
        """Tests "done" method.
        """
        
        class FakeMessageStorage(object):
            def add(*args, **kwargs):
                pass
                
        class FakeForm(object):
            cleaned_data = {}
            
        class SelectPluggetSourceFakeForm(FakeForm):
            cleaned_data = {"source_uid": "Test"}
            
        class CustomizePluggetFakeForm(FakeForm):
            cleaned_data = {"title": "Another Plugget", "text": "Something.", "user": self.u1}
                
        v = PluggetWizard()
        v.source = registry.get_plugget_source(self.p.source)
        
        v.request = self.factory.get(self.add_url)
        v.request._messages = FakeMessageStorage()
        
        try:
            instance = Plugget.objects.get(title="Another Plugget", context='{"text": "Something.", "user": 1}')
            self.fail()
        except Plugget.DoesNotExist:
            pass
            
        form_list = [SelectPluggetSourceFakeForm(), CustomizePluggetFakeForm()]
        
        response = v.done(form_list, slug=self.r.slug)
        
        self.assertEqual(response.url, self.r.get_absolute_url())
        
        try:
            instance = Plugget.objects.get(title="Another Plugget", context='{"text": "Something.", "user": 1}')
        except Plugget.DoesNotExist:
            self.fail()
        
        v.request = self.factory.get(resolve_url("plugget_edit", pk=instance.pk))
        v.request._messages = FakeMessageStorage()
        v.instance = instance
        
        form_list[1].cleaned_data["title"] = "A changed plugget"
        form_list[1].cleaned_data["text"] = "Something else."
        
        response = v.done(form_list, slug=self.r.slug)
        
        self.assertEqual(response.url, self.r.get_absolute_url())
        self.assertEqual(instance.title, "A changed plugget")
        self.assertEqual(instance.context, '{"text": "Something else.", "user": 1}')
        
        instance.delete()
        
class DeletePluggetViewTestCase(TestCase):
    def setUp(self):        
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
