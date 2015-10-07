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
from django.test.utils import override_settings
from django.shortcuts import resolve_url
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from . import FakeRequest
from ..models import User, ObjectPermission
from ..views import _get_user # Is not in the public API.
from ..views import *


class GetterTestCase(TestCase):
    def test_get_user_from_kwargs(self):
        """Tests retrieving a user instance from view's kwargs dict.
        """
        u1, n = User.objects.get_or_create(pk=1, username="u1")
        
        kwargs = {"pk": u1.pk}
        
        try:
            u = _get_user(None, **kwargs)
            self.assertEqual(u, u1)
        except User.DoesNotExist:
            self.assertFalse(True)

@override_settings(LOGIN_REQUIRED_URLS_EXCEPTIONS=(r'/(.*)$',))    
class SetCancelUrlMixinTestCase(TestCase):
    urls = 'djangoerp.core.tests.urls'
    
    def test_back_in_context_data(self):
        """Tests the presence of a "back" variable in context data.
        """
        response = self.client.get('/default_cancel_url/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data.get("back"), "/")
    
    def test_preset_cancel_url(self):
        """Tests setting of "cancel_url" variable to preset a default back url.
        """
        response = self.client.get('/preset_cancel_url/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data.get("back"), "/go_to_cancel_url/")
    
    def test_cancel_url_from_request(self):
        """Tests using a "cancel_url" retrieved from "request.GET".
        """
        response = self.client.get('/default_cancel_url/?back=/custom_cancel_url/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data.get("back"), "/custom_cancel_url/")
        
class BaseModelListViewTestCase(TestCase):
    def test_get_default_params(self):
        """Tests correct getting of view's default parameters.
        """
        v = BaseModelListView()
        
        self.assertEqual(v.field_list, None)
        self.assertEqual(v.get_field_list(), v.field_list)
        self.assertEqual(v.list_template_name, "elements/model_list.html")
        self.assertEqual(v.get_list_template_name(), v.list_template_name)
        self.assertEqual(v.list_uid, "")
        self.assertEqual(v.get_list_uid(), v.list_uid)
        self.assertEqual(v.get_list_prefix(), "")
        
    def test_get_list_prefix(self):
        """Tests correct handling of list prefix.
        """
        v = BaseModelListView(["uid"], "my_template.html", "my_list_uid")
        
        self.assertEqual(v.list_uid, "my_list_uid")
        self.assertEqual(v.get_list_uid(), v.list_uid)
        self.assertEqual(v.get_list_prefix(), "my_list_uid_")
     
    def test_paginate_queryset(self):
        """Tests correct handling of pagination based on list prefix.
        """
        v = BaseModelListView()
        v.kwargs = {}
        v.request = FakeRequest()
        
        v.paginate_queryset([], 1)
        
        self.assertEqual(v.page_kwarg, "page")
        
        v.list_uid = "my_list"
        v.paginate_queryset([], 1)
        
        self.assertEqual(v.page_kwarg, "my_list_page")
     
    def test_get_context_data(self):
        """Tests adding list-related variables to context dict.
        """
        v = BaseModelListView()
        v.kwargs = {}
        v.request = FakeRequest()
        v.object_list = []
        
        context = v.get_context_data()
        
        self.assertTrue("field_list" in context)
        self.assertEqual(context['field_list'], None)
        self.assertTrue("list_template_name" in context)
        self.assertEqual(context['list_template_name'], "elements/model_list.html")
        self.assertTrue("list_uid" in context)
        self.assertEqual(context['list_uid'], "")
        
class ModelListDeleteMixinTestCase(TestCase):
    def setUp(self):
        class FakeBase(object):
            page_kwarg = "page"
            
            def get(self, request, *args, **kwargs):
                return "get"
                
            def post(self, request, *args, **kwargs):
                return "post"
                
            def get_list_prefix(self):
                return ""
                
            def get_queryset(self):
                return get_user_model().objects.all()
                
            def get_paginate_by(self, qs):
                return int(max(1, qs.count()))
            
        class TestModelListDeleteMixin(ModelListDeleteMixin, FakeBase):
            pass
            
        self.request = FakeRequest()
        self.m = TestModelListDeleteMixin()
        
    def test_select_all_uids(self):
        """Tests selecting all UIDs in the model list.
        """
        self.request.POST = {"select_all": True}
        
        self.assertEqual(self.m.get_selected_uids(self.request), "*")
        
    def test_get_selected_uids(self):
        """Tests selecting any UIDs in the model list.
        """
        self.request.POST = {"select_1": True, "select_2": False, "select_3": True, "select_4": ""}
        
        self.assertEqual(
            sorted(self.m.get_selected_uids(self.request)),
            ["1", "3"]
        )
        
    def test_get_delete_template_name(self):
        """Tests retrieving delete template name.
        """
        self.assertEqual(self.m.delete_template_name, "base_model_list_confirm_delete.html")
        self.assertEqual(self.m.get_delete_template_name(), self.m.delete_template_name)
        
    def test_handle_as_get_when_has_no_selected_items(self):
        """Tests calling "get" (instead of "post") when no items are selected.
        """
        self.request.POST = {"select_all": True, "delete_selected": True}
        
        response = self.m.post(self.request)
        
        self.assertEqual(response, "get") # NOTE: convenient result just for test. 
        
    def test_post_to_confirm_deletion(self):
        """Tests performing confirm deletion after a proper POST request.
        """
        from django.template.response import TemplateResponse

        user_model = get_user_model()
        u1 = user_model.objects.create(username="u1")
        self.request.POST = {"select_all": True, "delete_selected": True}
        
        response = self.m.post(self.request)
        
        self.assertTrue(isinstance(response, TemplateResponse))
        self.assertEqual(response.template_name, self.m.get_delete_template_name())
        
    def test_post_to_deletion(self):
        """Tests performing real deletion after a proper POST request.
        """
        user_model = get_user_model()
        u1 = user_model.objects.create(username="u1")
        self.request.POST = {"select_all": True, "confirm_delete_selected": True}
        
        response = self.m.post(self.request)
        
        self.assertEqual(response, "get") # NOTE: convenient result just for test.  
        self.assertEqual(user_model.objects.count(), 0)
        
    def test_post_to_parent_post(self):
        """Tests redirecting to parent's POST when there's no need to delete.
        """
        self.request.POST = {}
        
        response = self.m.post(self.request)
        
        self.assertEqual(response, "post") # NOTE: convenient result just for test.
        
    def test_delete_all(self):
        """Tests deleting all items.
        """
        from django.template.response import TemplateResponse

        user_model = get_user_model()
        u1 = user_model.objects.create(username="u1")
        u2 = user_model.objects.create(username="u2")
        u3 = user_model.objects.create(username="u3")
        self.request.POST = {"delete_selected": True, "select_all": True}
        qs = self.m.get_queryset()
        
        # 1) Show confirm deletion template.
        self.assertQuerysetEqual(
            qs,
            list(map(repr, user_model.objects.all())),
            ordered=False
        )
        self.assertEqual(qs.count(), 3)
        
        response = self.m.delete_selected(self.request)
        
        self.assertTrue(isinstance(response, TemplateResponse))
        self.assertEqual(response.template_name, self.m.get_delete_template_name())
        self.assertQuerysetEqual(
            response.context_data['object_list'],
            list(map(repr, qs)),
            ordered=False
        )
        
        # 2) Delete all items.
        del self.request.POST['delete_selected']
        self.request.POST['confirm_delete_selected'] = True
        
        response = self.m.delete_selected(self.request)
        
        self.assertEqual(response, "get") # NOTE: convenient result just for test.
        self.assertEqual(user_model.objects.count(), 0)
        
    def test_delete_selected(self):
        """Tests deleting selected items.
        """
        from django.template.response import TemplateResponse

        user_model = get_user_model()
        u1 = user_model.objects.create(username="u1")
        u2 = user_model.objects.create(username="u2")
        u3 = user_model.objects.create(username="u3")
        self.request.POST = {"delete_selected": True, "select_1": True, "select_2": False, "select_3": True}
        qs = self.m.get_queryset()
        
        # 1) Show confirm deletion template.   
        self.assertQuerysetEqual(
            qs,
            list(map(repr, user_model.objects.all())),
            ordered=False
        )
        self.assertEqual(qs.count(), 3)
             
        response = self.m.delete_selected(self.request)
        
        self.assertTrue(isinstance(response, TemplateResponse))
        self.assertEqual(response.template_name, self.m.get_delete_template_name())
        self.assertQuerysetEqual(
            response.context_data['object_list'],
            list(map(repr, user_model.objects.filter(pk__in=[1, 3]))),
            ordered=False
        )
        
        # 2) Delete all items.
        del self.request.POST['delete_selected']
        self.request.POST['confirm_delete_selected'] = True
        
        response = self.m.delete_selected(self.request)
        
        self.assertEqual(response, "get") # NOTE: convenient result just for test.
        self.assertEqual(user_model.objects.count(), 1)
        self.assertQuerysetEqual(
            user_model.objects.values("pk"),
            [repr({'pk': 2})],
            ordered=False
        )
        
    def test_pagination_on_deletion(self):
        """Tests pagination handling after item deletion.
        """
        from django.http import HttpResponseRedirect
        
        def _new_get_paginate_by(qs):
            return 2
            
        old_get_paginate_by = self.m.get_paginate_by
            
        self.m.get_paginate_by = _new_get_paginate_by

        user_model = get_user_model()
        u1 = user_model.objects.create(username="u1")
        u2 = user_model.objects.create(username="u2")
        u3 = user_model.objects.create(username="u3")
        u4 = user_model.objects.create(username="u4")
        u5 = user_model.objects.create(username="u5")
        self.request.GET = {"page": 3}
        self.request.POST = {"confirm_delete_selected": True, "select_5": True}
        
        response = self.m.delete_selected(self.request)
        
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.url, "/home/test/?page=2")
        self.assertEqual(user_model.objects.count(), 4)
        
        # Restores previous behavior.
        self.m.get_paginate_by = old_get_paginate_by

class ModelListFilteringMixinTestCase(TestCase):
    def setUp(self):
        user_model = get_user_model()
        
        class FakeBase(object):
            def get_queryset(self):
                return user_model.objects.all()
                
            def get_list_prefix(self):
                return ""
                
            def get_context_data(self):
                return {}
                
        class TestModelListFilteringMixin(ModelListFilteringMixin, FakeBase):
            pass

        self.m = TestModelListFilteringMixin()
        self.m.request = FakeRequest()
        self.u1 = user_model.objects.create(username="u1", email="u1@u.it")
        self.u2 = user_model.objects.create(username="u2", email="u2@u.it")
        self.u3 = user_model.objects.create(username="u3", email="u3@u.it")
        self.u4 = user_model.objects.create(username="u4", email="u4@u.it")
        
    def test_get_queryset(self):
        """Tests returning filtered queryset.
        """
        user_model = get_user_model()
        
        self.m.request.GET = {}
        qs = self.m.get_queryset()
        
        self.assertEqual(qs.count(), 4)
        self.assertQuerysetEqual(
            qs,
            list(map(repr, user_model.objects.all())),
            ordered=False
        )
        
        self.m.request.GET = {"filter_by_username__lt": "u4"}
        qs = self.m.get_queryset()
        
        self.assertEqual(qs.count(), 3)
        self.assertQuerysetEqual(
            qs,
            list(map(repr, user_model.objects.filter(username__lt="u4"))),
            ordered=False
        )
        
        self.m.request.GET = {"filter_by_username__lt": "u4", "filter_by_email__gte": "u2@u.it"}
        qs = self.m.get_queryset()
        
        self.assertEqual(qs.count(), 2)
        self.assertQuerysetEqual(
            qs,
            list(map(repr, user_model.objects.filter(username__lt="u4", email__gte="u2@u.it"))),
            ordered=False
        )
        self.assertQuerysetEqual(
            qs,
            [repr(self.u2), repr(self.u3)],
            ordered=False
        )
        
    def test_get_context_data(self):
        """Tests returning correct context variables.
        """
        user_model = get_user_model()
        
        self.m.request.GET = {"filter_by_username__lt": "u4", "filter_by_email__gte": "u2@u.it"}
        context = self.m.get_context_data()
        
        self.assertTrue("unfiltered_object_list" in context)
        self.assertQuerysetEqual(
            context['unfiltered_object_list'],
            list(map(repr, user_model.objects.all())),
            ordered=False
        )
        
        self.assertTrue("list_filter_by" in context)
        self.assertEqual(
            context['list_filter_by'],
            {
                "username": ("lt", "u4"),
                "email": ("gte", "u2@u.it"),
            }
        )
        
    def test_post(self):
        """Tests correct handling of POST requests.
        """
        self.m.request.GET = {}
        self.m.request.POST = {}
        response = self.m.post(self.m.request)
        
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.url, "/home/test/")
        
        self.m.request.POST = {
            "filter_by_username": "u4", "filter_expr_username": "lt",
            "filter_by_email": "u2@u.it", "filter_expr_email": "gte"
        }
        response = self.m.post(self.m.request)
        
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.url, "/home/test/?filter_by_email__gte=u2@u.it;filter_by_username__lt=u4")
        
    def test_reset_filters(self):
        """Tests resetting (clearing) filters.
        """
        self.m.request.GET = {}
        self.m.request.POST = {
            "filter_by_username": "u4", "filter_expr_username": "lt",
            "filter_by_email": "u2@u.it", "filter_expr_email": "gte",
            "reset_filters": True
        }
        response = self.m.post(self.m.request)
        
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.url, "/home/test/")
        
    def test_get_filter_query_from_post(self):
        """Tests getting correct filter query from POST request.
        """
        self.m.request.GET = {}
        self.m.request.POST = {}
        filter_query = self.m.get_filter_query_from_post()
        
        self.assertEqual(filter_query, {})
        
        self.m.request.POST = {
            "filter_by_username": "u4", "filter_expr_username": "lt",
            "filter_by_email": "u2@u.it", "filter_expr_email": "gte",
            "filter_by_is_staff": True,
        }
        filter_query = self.m.get_filter_query_from_post()
        
        self.assertEqual(filter_query, {"email__gte": "u2@u.it", "username__lt": "u4", "is_staff": True})
        
    def test_get_filter_query_from_get(self):
        """Tests getting correct filter query from GET request.
        """
        self.m.request.GET = {}
        self.m.request.POST = {}
        filter_query = self.m.get_filter_query_from_get()
        
        self.assertEqual(filter_query, {})
        
        self.m.request.GET = {
            "filter_by_username__lt": "u4",
            "filter_by_email__gte": "u2@u.it",
            "filter_by_is_staff": True,
        }
        filter_query = self.m.get_filter_query_from_get()
        
        self.assertEqual(filter_query, {"email__gte": "u2@u.it", "username__lt": "u4", "is_staff": True})

class ModelListOrderingMixinTestCase(TestCase):
    def setUp(self):
        user_model = get_user_model()
        
        class FakeBase():
            def get_queryset(self):
                return user_model.objects.all()
                
            def get_list_prefix(self):
                return ""
                
            def get_context_data(self):
                return {}
                
        class TestModelListOrderingMixin(ModelListOrderingMixin, FakeBase):
            pass
            
        self.m = TestModelListOrderingMixin()
        self.m.request = FakeRequest()
        self.u1 = user_model.objects.create(username="Anna", email="z@z.it")
        self.u2 = user_model.objects.create(username="Berta", email="ab@a.it")
        self.u3 = user_model.objects.create(username="Wendy", email="aa@g.it")
        self.u4 = user_model.objects.create(username="Grace", email="g@g.it")
        
    def test_get_queryset(self):
        """Tests returning ordered queryset.
        """
        user_model = get_user_model()
        
        self.m.request.GET = {}
        qs = self.m.get_queryset()
        
        self.assertEqual(
            list(map(repr, qs)),
            list(map(repr, user_model.objects.all())),
        )
        
        self.m.request.GET = {"order_by": "username"}
        qs = self.m.get_queryset()
        
        self.assertEqual(
            list(map(repr, qs)),
            list(map(repr, user_model.objects.order_by("username"))),
        )
        
        self.m.request.GET = {"order_by": "-username"}
        qs = self.m.get_queryset()
        
        self.assertEqual(
            list(map(repr, qs)),
            list(map(repr, user_model.objects.order_by("-username"))),
        )
        
        self.m.request.GET = {"order_by": "email"}
        qs = self.m.get_queryset()
        
        self.assertEqual(
            list(map(repr, qs)),
            list(map(repr, user_model.objects.order_by("email"))),
        )
        
    def test_get_context_data(self):
        """Tests returning correct context variables.
        """
        user_model = get_user_model()
        
        self.m.request.GET = {}
        context = self.m.get_context_data()
        
        self.assertTrue("list_order_by" in context)
        self.assertEqual(context['list_order_by'], None)
        
        self.m.request.GET = {"order_by": "username"}
        context = self.m.get_context_data()
        
        self.assertTrue("list_order_by" in context)
        self.assertEqual(context['list_order_by'], "username")
        
        self.m.request.GET = {"order_by": "-username"}
        context = self.m.get_context_data()
        
        self.assertTrue("list_order_by" in context)
        self.assertEqual(context['list_order_by'], "-username")
        
        self.m.request.GET = {"order_by": "email"}
        context = self.m.get_context_data()
        
        self.assertTrue("list_order_by" in context)
        self.assertEqual(context['list_order_by'], "email")
        
class DetailUserViewTestCase(TestCase):
    def setUp(self):
        self.u1 = get_user_model().objects.create_user("u1", "u@u.it", "password")
        self.u2 = get_user_model().objects.create_user("u2", "u@u.it", "password")
        
    def test_deny_anonymous_user(self):
        """Tests anonymous users can not access the view.
        """
        self.client.logout()
        response = self.client.get(resolve_url("user_detail", pk=self.u2.pk))
        
        self.assertEqual(response.status_code, 302)
        
    def test_logged_user_without_perms(self):
        """Tests logged users (but without correct perms) can not access the view.
        """
        self.client.login(username='u1', password='password')
        response = self.client.get(resolve_url("user_detail", pk=self.u2.pk))
        
        self.assertEqual(response.status_code, 302)
        
    def test_logged_user_with_perms(self):
        """Tests logged users with correct perms can access the view.
        """
        p, n = ObjectPermission.objects.get_or_create_by_natural_key("view_user", "core", "user", self.u2.pk)
        self.u2.objectpermissions.add(p)
        
        self.client.login(username='u2', password='password')
        response = self.client.get(resolve_url("user_detail", pk=self.u2.pk))
        
        self.assertEqual(response.status_code, 200)

class UpdateUserViewTestCase(TestCase):
    def setUp(self):
        self.u1 = get_user_model().objects.create_user("u1", "u@u.it", "password")
        self.u2 = get_user_model().objects.create_user("u2", "u@u.it", "password")
        
    def test_deny_anonymous_user(self):
        """Tests anonymous users can not access the view.
        """
        self.client.logout()
        response = self.client.get(resolve_url("user_edit", pk=self.u2.pk))
        
        self.assertEqual(response.status_code, 302)
        
    def test_logged_user_without_perms(self):
        """Tests logged users (but without correct perms) can not access the view.
        """
        self.client.login(username='u1', password='password')
        response = self.client.get(resolve_url("user_edit", pk=self.u2.pk))
        
        self.assertEqual(response.status_code, 302)
        
    def test_logged_user_with_perms(self):
        """Tests logged users with correct perms can access the view.
        """
        p, n = ObjectPermission.objects.get_or_create_by_natural_key("change_user", "core", "user", self.u2.pk)
        self.u2.objectpermissions.add(p)
        
        self.client.login(username='u2', password='password')
        response = self.client.get(resolve_url("user_edit", pk=self.u2.pk))
        
        self.assertEqual(response.status_code, 200)

class DeleteUserViewTestCase(TestCase):
    def setUp(self):
        self.u1 = get_user_model().objects.create_user("u1", "u@u.it", "password")
        self.u2 = get_user_model().objects.create_user("u2", "u@u.it", "password")
        
    def test_deny_anonymous_user(self):
        """Tests anonymous users can not access the view.
        """
        self.client.logout()
        response = self.client.get(resolve_url("user_delete", pk=self.u2.pk))
        
        self.assertEqual(response.status_code, 302)
        
    def test_logged_user_without_perms(self):
        """Tests logged users (but without correct perms) can not access the view.
        """
        self.client.login(username='u1', password='password')
        response = self.client.get(resolve_url("user_delete", pk=self.u2.pk))
        
        self.assertEqual(response.status_code, 302)
        
    def test_logged_user_with_perms(self):
        """Tests logged users with correct perms can access the view.
        """
        p, n = ObjectPermission.objects.get_or_create_by_natural_key("delete_user", "core", "user", self.u2.pk)
        self.u2.objectpermissions.add(p)
        
        self.client.login(username='u2', password='password')
        response = self.client.get(resolve_url("user_delete", pk=self.u2.pk))
        
        self.assertEqual(response.status_code, 200)
        
    def test_success_url_on_current_user_deletion(self):
        """Tests returned "success_url" when the current user is deleted.
        """
        view = DeleteUserView()
        
        view.kwargs = {'pk': self.u2.pk}
        view.request = FakeRequest()
        view.request.user = self.u2
        view.get_object()
        
        self.assertEqual(view.success_url, resolve_url("user_logout"))
        
    def test_success_url_on_different_user_deletion(self):
        """Tests returned "success_url" when a different user is deleted.
        """
        view = DeleteUserView()
        
        view.kwargs = {'pk': self.u1.pk}
        view.request = FakeRequest()
        view.request.user = self.u2
        view.get_object()
        
        self.assertEqual(view.success_url, "/")
