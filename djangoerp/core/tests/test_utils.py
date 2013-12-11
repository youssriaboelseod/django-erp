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
__version__ = '0.0.2'

from django.test import TestCase
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

from . import *
from ..models import Group
from ..utils import *
from ..utils.dependencies import *
from ..utils.rendering import *
          
class GetModelTestCase(TestCase):
    def test_invalid_klass(self):
        """Tests "get_model" func must raise a ValueError.
        """
        try:
            m = get_model(None)
            self.fail()
        except ValueError:
            pass
            
    def test_model_klass(self):
        """Tests "get_model" func when a real model class is passed.
        """
        try:
            m = get_model(get_user_model())
            self.assertEqual(m, get_user_model())
        except ValueError:
            self.fail()
            
    def test_model_instance(self):
        """Tests "get_model" func when a real model instance is passed.
        """
        try:
            u, n = get_user_model().objects.get_or_create(username="user_instance")
            m = get_model(u)
            self.assertEqual(m, get_user_model())
        except ValueError:
            self.fail()
            
    def test_model_queryset(self):
        """Tests "get_model" func when a real model queryset is passed.
        """
        try:
            qs = get_user_model().objects.all()
            m = get_model(qs)
            self.assertEqual(m, get_user_model())
        except ValueError:
            self.fail()
            
    def test_model_string(self):
        """Tests "get_model" func when a model string is passed.
        """
        try:
            m = get_model(user_model_string)
            self.assertEqual(m, get_user_model())
        except ValueError:
            self.fail()
          
class CleanHTTPRefererTestCase(TestCase):
    def test_no_request(self):
        """Tests when there isn't a request, default_referer must be returned.
        """
        default_referer = '/'
        self.assertEqual(clean_http_referer(None, default_referer), default_referer)
            
    def test_other_site_referer(self):
        """Tests that a valid referer is correctly returned by the function.
        """
        request = FakeRequest()
        self.assertEqual(clean_http_referer(request), "www.test.com")
            
    def test_host_strip_referer(self):
        """Tests the current host should be stripped out.
        """
        expected_referer = '/test'
        request = FakeRequest()
        request.META["HTTP_REFERER"] = request.META['HTTP_HOST'] + expected_referer
        self.assertEqual(clean_http_referer(request), expected_referer)
        
    def test_silently_fail_when_no_http_host(self):
        """Tests that no error should be raised when request hasn't a HTTP_HOST.
        """
        request = FakeRequest()
        del request.META['HTTP_HOST']
        try:
            clean_http_referer(request)
        except:
            self.fail("Failure caused by the absence of HTTP_HOST variable.")
        
class SetPathKwargsTestCase(TestCase):
    def setUp(self):
        self.request = FakeRequest()
        self.request.GET = {
            "next": "/home/",
            "prev": "/home/test/foo/",
            "filter_by": "name",
        }
        
    def test_appending_no_kwargs(self):
        """Tests returning the path as is.
        """
        self.assertEqual(
            set_path_kwargs(FakeRequest()),
            "/home/test/"
        )
        
    def test_appending_get_kargs(self):
        """Tests appending kwargs from request.GET.
        """
        self.assertEqual(
            set_path_kwargs(self.request),
            "/home/test/?next=/home/;prev=/home/test/foo/;filter_by=name"
        )
        
    def test_filtering_existing_kwargs(self):
        """Tests filtering out existing kwargs.
        """
        self.assertEqual(
            set_path_kwargs(self.request, filter_by="id", prev="/"),
            "/home/test/?prev=/;filter_by=id;next=/home/"
        )
        
    def test_removing_invalid_kwargs(self):
        """Tests removing invalid kwargs.
        """
        self.assertEqual(
            set_path_kwargs(self.request, filter_by=None, prev="/"),
            "/home/test/?prev=/;next=/home/"
        )
        
class DependencyTestCase(TestCase):
    def test_satisfied_dependency(self):
        """Tests that when a dependency is satisfied, no error is raised.
        """
        try:
          check_dependency("djangoerp.core")
        except DependencyError:
          self.fail()

    def test_not_satisfied_dependency(self):
        """Tests that when a dependency is not satisfied, an error must be raised.
        """
        try:
          check_dependency("supercalifragidilistichespiralidoso.core")
          self.fail()
        except DependencyError as e:
          self.assertEqual("%s" % e, u"A dependency is not satisfied: supercalifragidilistichespiralidoso.core")

class RenderingValueToStringTestCase(TestCase):
    def test_empty_value_to_string(self):
        """Tests rendering of an empty value.
        """
        self.assertEqual(value_to_string(None), mark_safe(render_to_string('elements/empty.html', {})))

    def test_bool_true_value_to_string(self):
        """Tests rendering of a valid boolean value.
        """
        self.assertEqual(value_to_string(True), mark_safe(render_to_string('elements/yes.html', {})))

    def test_bool_true_value_to_string(self):
        """Tests rendering of an invalid boolean value.
        """
        self.assertEqual(value_to_string(False), mark_safe(render_to_string('elements/no.html', {})))

    def test_float_value_to_string(self):
        """Tests rendering of a float value.
        """
        self.assertEqual(value_to_string(2.346), '2.35')

    def test_integer_value_to_string(self):
        """Tests rendering of an integer value.
        """
        self.assertEqual(value_to_string(2346), '2346')

    def test_list_value_to_string(self):
        """Tests rendering of a list.
        """
        self.assertEqual(value_to_string([None, True]), '%s, %s' % (mark_safe(render_to_string('elements/empty.html', {})), mark_safe(render_to_string('elements/yes.html', {}))))

    def test_tuple_value_to_string(self):
        """Tests rendering of a list.
        """
        self.assertEqual(value_to_string((None, False)), '%s, %s' % (mark_safe(render_to_string('elements/empty.html', {})), mark_safe(render_to_string('elements/no.html', {}))))
        
class RenderingFieldToValueTestCase(TestCase):
    def setUp(self):
        user_model = get_user_model()    
        
        self.u1 = user_model.objects.create(username="u1")     
        
        class TestModelInstance(models.Model):
            id = models.PositiveIntegerField(default=5, primary_key=True)
            user = models.ForeignKey(user_model, default=self.u1.pk)
            group = models.ForeignKey(Group, default=self.u1.groups.first().pk)
            slug = models.SlugField(default="fake_object")
            url = models.URLField(default="http://localhost:8000/test")
            email = models.EmailField(default="u@u.it")
            choice = models.TextField(default="test", choices=[("test", "A test")])
            flag = models.BooleanField(default=True)
                
        self.test_obj = TestModelInstance()
        self.field_list = dict([(f.name, f) for f in (self.test_obj._meta.fields)])
        self.m2m_list = dict([(f.name, f) for f in (self.u1._meta.many_to_many)])
                
    def test_primary_key_field(self):
        """Tests conversion of a primary key field.
        """
        self.assertEqual(
            field_to_value(self.field_list['id'], self.test_obj),
            "#5"
        )
                
    def test_foreign_key_field(self):
        """Tests conversion of a foreign key field.
        """
        self.assertEqual(
            field_to_value(self.field_list['user'], self.test_obj),
            mark_safe(render_to_string('elements/link.html', {"url": self.u1.get_absolute_url(), "caption": u"%s" % self.u1}))
        )
        
        self.assertEqual(
            field_to_value(self.field_list['group'], self.test_obj).pk,
            self.u1.groups.first().pk
        )
                
    def test_m2m_field(self):
        """Tests conversion of a m2m relationship field.
        """
        self.assertEqual(
            field_to_value(self.m2m_list['groups'], self.u1),
            ["users"]
        )
                
    def test_slug_field(self):
        """Tests conversion of a slug field.
        """
        self.assertEqual(
            field_to_value(self.field_list['slug'], self.test_obj),
            "#fake_object"
        )
                
    def test_url_field(self):
        """Tests conversion of an URL field.
        """
        self.assertEqual(
            field_to_value(self.field_list['url'], self.test_obj),
            mark_safe(render_to_string('elements/link.html', {"url": "http://localhost:8000/test", "caption": "http://localhost:8000/test"}))
        )
                
    def test_email_field(self):
        """Tests conversion of an email field.
        """
        self.assertEqual(
            field_to_value(self.field_list['email'], self.test_obj),
            mark_safe(render_to_string('elements/link.html', {"url": "mailto:u@u.it", "caption": "u@u.it"}))
        )
                
    def test_choice_field(self):
        """Tests conversion of a field with choices.
        """
        self.assertEqual(
            field_to_value(self.field_list['choice'], self.test_obj),
            self.test_obj.get_choice_display()
        )
                
    def test_boolean_field(self):
        """Tests conversion of a boolean field.
        """
        self.assertEqual(
            field_to_value(self.field_list['flag'], self.test_obj),
            True
        )
        
        self.test_obj.flag = False
        
        self.assertEqual(
            field_to_value(self.field_list['flag'], self.test_obj),
            False
        )
