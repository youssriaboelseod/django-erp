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
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from . import *
from ..templatetags.introspection import *
from ..templatetags.markup import *
from ..templatetags.perms import *
from ..templatetags.breadcrumbs import *
from ..templatetags.avatar import *
        

class JoinStringsTemplateTagTestCase(TestCase):
    def test_join_list_with_empty_string(self):
        """Tests "join" templatetag must exclude empty/invalid strings.
        """
        self.assertEqual(join("_", "a", "b", "", "d"), "a_b_d")
        
class SplitFilterTestCase(TestCase):
    def test_split_on_string(self):
        """Tests the split filter on a string.
        """
        self.assertEqual(split("a/path/to/my/folder", '/'), ["a", "path", "to", "my", "folder"])
        
class DiffFilterTestCase(TestCase):
    def test_diff_with_number(self):
        """Tests the diff filter using a number.
        """
        self.assertEqual(diff(5, 2), 3)
        
    def test_diff_with_string(self):
        """Tests the diff filter using a numeric string.
        """
        self.assertEqual(diff(5, "2"), 3)
        
class GetFilterTestCase(TestCase):
    def test_get_from_dict(self):
        """Tests getting a value from a dict.
        """
        self.assertEqual(get({"foo": "bar"}, "foo"), "bar")
        
    def test_get_from_list(self):
        """Tests getting a value from a list.
        """
        self.assertEqual(get(["foo", "bar"], 1), "bar")
        
    def test_get_from_tuple(self):
        """Tests getting a value from a tuple.
        """
        self.assertEqual(get(("foo", "bar"), 1), "bar")
        
    def test_get_invalid_from_list_or_tuple(self):
        """Tests getting a value from a tuple.
        """
        self.assertEqual(get(["foo", "bar"], "foo"), "")
        self.assertEqual(get(("foo", "bar"), "foo"), "")
        
    def test_get_from_object(self):
        """Tests getting a value from an object.
        """
        class TestObject:
            foo = "bar"
            
            def foo_func(self): return "bar_func"
            
        obj = TestObject()
            
        self.assertEqual(get(obj, "foo"), "bar")
        self.assertEqual(get(obj, "foo_func"), "bar_func")
    
class ModelNameFilterTestCase(TestCase):
    def test_valid_model_name(self):
        """Tests returning of a valid model name using "model_name" filter.
        """
        self.assertEqual(model_name(get_user_model()), "user") 
        self.assertEqual(model_name(get_user_model()), "user")
        
    def test_invalid_model_name(self):
        """Tests "model_name" filter on an invalid input.
        """
        class FakeObject:
            pass
            
        self.assertEqual(model_name(FakeObject), "") 
        self.assertEqual(model_name(FakeObject()), "")
        
    def test_plural_model_name(self):
        """Tests returning of a plural model name using "model_name" filter.
        """
        self.assertEqual(model_name_plural(get_user_model()), "users") 
        self.assertEqual(model_name_plural(get_user_model()), "users")
        
    def test_invalid_plural_model_name(self):
        """Tests "model_name_plural" filter on an invalid input.
        """
        class FakeObject:
            pass
            
        self.assertEqual(model_name_plural(FakeObject), "") 
        self.assertEqual(model_name_plural(FakeObject()), "")
        
    def test_proxy_model_name(self):
        """Tests proxy-model name must be returned instead of concrete one.
        """
        class ProxyUser(get_user_model()):
            class Meta:
                proxy = True
                verbose_name = 'proxy user'
                verbose_name_plural = 'proxy users'
                
        self.assertEqual(model_name(ProxyUser), 'proxy user')
        self.assertEqual(model_name(ProxyUser()), 'proxy user')
        self.assertEqual(model_name_plural(ProxyUser), 'proxy users')
        self.assertEqual(model_name_plural(ProxyUser()), 'proxy users')
        
    def test_valid_raw_model_name(self):
        """Tests returning of a valid model name using "raw_model_name" filter.
        """
        self.assertEqual(raw_model_name(get_user_model()), "user") 
        self.assertEqual(raw_model_name(get_user_model()), "user")
        
    def test_invalid_raw_model_name(self):
        """Tests "raw_model_name" filter on an invalid input.
        """
        class FakeObject:
            pass
            
        self.assertEqual(raw_model_name(FakeObject), "") 
        self.assertEqual(raw_model_name(FakeObject()), "")
        
    def test_plural_raw_model_name(self):
        """Tests returning of a plural model name using "raw_model_name_plural" filter.
        """
        self.assertEqual(raw_model_name_plural(get_user_model()), "users") 
        self.assertEqual(raw_model_name_plural(get_user_model()), "users")
        
    def test_invalid_plural_raw_model_name(self):
        """Tests "raw_model_name_plural" filter on an invalid input.
        """
        class FakeObject:
            pass
            
        self.assertEqual(raw_model_name_plural(FakeObject), "") 
        self.assertEqual(raw_model_name_plural(FakeObject()), "")
        
class ModelListTagTestCase(TestCase):
    def test_render_model_list_from_invalid_object_list(self):
        """Tests rendering a model list from an invalid object_list (not a queryset).
        """
        self.assertEqual(
            render_model_list({}, None),
            ""
        )
        
    def test_render_empty_model_list(self):
        """Tests rendering an empty model list table.
        """
        qs = get_user_model().objects.none()
        table_dict = {
            "uid": "",
            "order_by": [],
            "headers": [
                {"name": "username", "attname": "username", "type": "char", "filter": {"expr": "", "value": ""}}
            ],
            "rows": [
            ]
        }
        
        self.assertEqual(
            render_model_list({}, qs, ["username"]),
            render_to_string("elements/model_list.html", {"table": table_dict})
        )
        
    def test_render_empty_model_list_with_uid(self):
        """Tests rendering an empty model list table with a custom UID.
        """
        qs = get_user_model().objects.none()
        table_dict = {
            "uid": "mytable",
            "order_by": [],
            "headers": [
                {"name": "username", "attname": "username", "type": "char", "filter": {"expr": "", "value": ""}}
            ],
            "rows": [
            ]
        }
        
        self.assertEqual(
            render_model_list({}, qs, ["username"], uid="mytable"),
            render_to_string("elements/model_list.html", {"table": table_dict})
        )
        
    def test_render_model_list_with_empty_field_list(self):
        """Tests rendering a model list with empty field_list (all fields used).
        """
        table_dict = {
            "uid": "",
            "order_by": [],
            "headers": [
                {"name": "ID", "attname": "id", "type": "auto", "filter": {"expr": "", "value": ""}},
                {"name": "name", "attname": "name", "type": "char", "filter": {"expr": "", "value": ""}}
            ],
            "rows": [
            ]
        }
        
        qs = Group.objects.none()
        rendered_table = render_to_string("elements/model_list.html", {"table": table_dict})
        
        self.assertEqual(
            render_model_list({}, qs),
            rendered_table
        )
        
        self.assertEqual(
            render_model_list({}, qs, None),
            rendered_table
        )
        
        self.assertEqual(
            render_model_list({}, qs, False),
            rendered_table
        )
        
    def test_render_one_row_model_list(self):
        """Tests rendering a model list table with one model instances.
        """
        u1, n = get_user_model().objects.get_or_create(username="u1")
        qs = get_user_model().objects.filter(username=u1.username)
        table_dict = {
            "uid": "",
            "order_by": [],
            "headers": [
                {"name": "username", "attname": "username", "type": "char", "filter": {"expr": "", "value": ""}}
            ],
            "rows": [
                {"object": u1, "fields": [u1.username]}
            ]
        }
        
        self.assertEqual(
            render_model_list({}, qs, ["username"]),
            render_to_string("elements/model_list.html", {"table": table_dict})
        )
        
    def test_render_model_list(self):
        """Tests rendering a model list table with many model instances.
        """
        u1, n = get_user_model().objects.get_or_create(username="u1")
        u2, n = get_user_model().objects.get_or_create(username="u2")
        u3, n = get_user_model().objects.get_or_create(username="u3")
        qs = get_user_model().objects.all()
        table_dict = {
            "uid": "",
            "order_by": [],
            "headers": [
                {"name": "username", "attname": "username", "type": "char", "filter": {"expr": "", "value": ""}}
            ],
            "rows": [
                {"object": u1, "fields": [u1.username]},
                {"object": u2, "fields": [u2.username]},
                {"object": u3, "fields": [u3.username]}
            ]
        }
        
        self.assertEqual(
            render_model_list({}, qs, ["username"]),
            render_to_string("elements/model_list.html", {"table": table_dict})
        )
        
    def test_render_ordered_model_list(self):
        """Tests rendering a model list table with an ordered queryset.
        """
        u1, n = get_user_model().objects.get_or_create(username="u1")
        u2, n = get_user_model().objects.get_or_create(username="u2")
        u3, n = get_user_model().objects.get_or_create(username="u3")
        
        qs = get_user_model().objects.order_by("-username")
        table_dict = {
            "uid": "",
            "order_by": [],
            "headers": [
                {"name": "username", "attname": "username", "type": "char", "filter": {"expr": "", "value": ""}}
            ],
            "rows": [
                {"object": u3, "fields": [u3.username]},
                {"object": u2, "fields": [u2.username]},
                {"object": u1, "fields": [u1.username]}
            ]
        }
        
        self.assertEqual(
            render_model_list({}, qs, ["username"]),
            render_to_string("elements/model_list.html", {"table": table_dict})
        )
        
        qs = get_user_model().objects.order_by("username")
        table_dict.update({
            "order_by": ["username"],
            "rows": [
                {"object": u1, "fields": [u1.username]},
                {"object": u2, "fields": [u2.username]},
                {"object": u3, "fields": [u3.username]}
            ]
        })
        
        self.assertEqual(
            render_model_list({}, qs, ["username"]),
            render_to_string("elements/model_list.html", {"table": table_dict})
        )
        
    def test_render_filtered_model_list(self):
        """Tests rendering a model list table with a filtered queryset.
        """
        u1, n = get_user_model().objects.get_or_create(username="u1")
        u2, n = get_user_model().objects.get_or_create(username="u2")
        u3, n = get_user_model().objects.get_or_create(username="u3")
        
        qs = get_user_model().objects.filter(username__lt="u3")
        table_dict = {
            "uid": "",
            "order_by": [],
            "headers": [
                {"name": "username", "attname": "username", "type": "char", "filter": {"expr": "lt", "value": "u3"}}
            ],
            "rows": [
                {"object": u1, "fields": [u1.username]},
                {"object": u2, "fields": [u2.username]},
            ]
        }
        
        self.assertEqual(
            render_model_list({"list_filter_by": {"username": ("lt", "u3")}}, qs, ["username"]),
            render_to_string("elements/model_list.html", {"table": table_dict})
        )
        
class ModelDetailsTagTestCase(TestCase):
    def test_render_empty_model_details(self):
        """Tests rendering an empty model details table.
        """
        details_dict = {
            "uid": "",
            "num_cols": 0,
            "layout": []
        }
        
        self.assertEqual(
            render_model_details({}, ""),
            render_to_string("elements/model_details.html", {"details": details_dict})
        )
        
    def test_render_empty_model_details_with_uid(self):
        """Tests rendering an empty model details table with a custom UID.
        """
        details_dict = {
            "uid": "mydetails",
            "num_cols": 0,
            "layout": []
        }
        
        self.assertEqual(
            render_model_details({}, "", uid="mydetails"),
            render_to_string("elements/model_details.html", {"details": details_dict})
        )
        
    def test_render_one_object_model_details(self):
        """Tests rendering a model details table with one model instances.
        """
        u1, n = get_user_model().objects.get_or_create(username="u1")
        
        details_dict = {
            "uid": "",
            "num_cols": 1,
            "layout": [[{"name": "Username:", "attrs": "", "value": "u1"}]]
        }
        
        self.assertEqual(
            render_model_details({}, u1, ['username']),
            render_to_string("elements/model_details.html", {"details": details_dict})
        )
        
    def test_render_more_objects_model_details(self):
        """Tests rendering a model details table with multiple model instances.
        """
        u1, n = get_user_model().objects.get_or_create(username="u1")
        u2, n = get_user_model().objects.get_or_create(username="u2")
        
        details_dict = {
            "uid": "",
            "num_cols": 1,
            "layout": [
                [{"name": "Username:", "attrs": "", "value": "u1"}],
                [{"name": "Username:", "attrs": "", "value": "u2"}],
            ]
        }
        
        self.assertEqual(
            render_model_details({}, [u1, u2], ['0.username', '1.username']),
            render_to_string("elements/model_details.html", {"details": details_dict})
        )
        
    def test_render_multiple_column_model_details(self):
        """Tests rendering a model details table with more columns on one row.
        """
        u1, n = get_user_model().objects.get_or_create(username="u1")
        u2, n = get_user_model().objects.get_or_create(username="u2")
        
        details_dict = {
            "uid": "",
            "num_cols": 2,
            "layout": [
                [{"name": "Username:", "attrs": "", "value": "u1"}, {"name": "Username:", "attrs": "", "value": "u2"}],
            ]
        }
        
        self.assertEqual(
            render_model_details({}, [u1, u2], [['0.username', '1.username']]),
            render_to_string("elements/model_details.html", {"details": details_dict})
        )
        
    def test_render_model_details_with_suffixes(self):
        """Tests rendering a model details table which uses custom suffixes.
        """
        u1, n = get_user_model().objects.get_or_create(username="u1")
        u2, n = get_user_model().objects.get_or_create(username="u2")
        
        details_dict = {
            "uid": "",
            "num_cols": 1,
            "layout": [
                [{"name": "Username:", "attrs": "", "value": "u1 (user)"}],
                [{"name": "Username:", "attrs": "", "value": "u2 (another user)"}],
            ]
        }
        
        self.assertEqual(
            render_model_details({}, [u1, u2], ['0.username:(user)', '1.username:(another user)']),
            render_to_string("elements/model_details.html", {"details": details_dict})
        )
        
    def test_render_model_details_with_string_objects(self):
        """Tests rendering a model details table passing objects as context keys.
        """
        u1, n = get_user_model().objects.get_or_create(username="u1")
        u2, n = get_user_model().objects.get_or_create(username="u2")
        
        details_dict = {
            "uid": "",
            "num_cols": 1,
            "layout": [
                [{"name": "Username:", "attrs": "", "value": "u1 (user)"}],
                [{"name": "Username:", "attrs": "", "value": "u2 (another user)"}],
            ]
        }
        
        self.assertEqual(
            render_model_details({"u1": u1, "u2": u2}, "[u1, u2]", ['0.username:(user)', '1.username:(another user)']),
            render_to_string("elements/model_details.html", {"details": details_dict})
        )
        
    def test_render_model_details_with_string_layout(self):
        """Tests rendering a model details table passing the layout as a string.
        """
        u1, n = get_user_model().objects.get_or_create(username="u1")
        u2, n = get_user_model().objects.get_or_create(username="u2")
        
        details_dict = {
            "uid": "",
            "num_cols": 1,
            "layout": [
                [{"name": "Username:", "attrs": "", "value": "u1 (user)"}],
                [{"name": "Username:", "attrs": "", "value": "u2 (another user)"}],
            ]
        }
        
        self.assertEqual(
            render_model_details({}, [u1, u2], "['0.username:(user)', '1.username:(another user)']"),
            render_to_string("elements/model_details.html", {"details": details_dict})
        )
        
    def test_render_model_details_without_layout(self):
        """Tests rendering a model details table without passing a layout.
        """
        g, n = Group.objects.get_or_create(name="g")
        
        details_dict = {
            "uid": "",
            "num_cols": 1,
            "layout": [
                [{"name": "Permissions:", "attrs": "", "value": mark_safe(render_to_string("elements/empty.html").strip())}],
                [{"name": "ID:", "attrs": "", "value": "#%d" % g.pk}],
                [{"name": "Name:", "attrs": "", "value": g.name}],
            ]
        }
        
        self.assertEqual(
            render_model_details({}, g),
            render_to_string("elements/model_details.html", {"details": details_dict})
        )
        
class UserHasPermTagTestCase(TestCase):
    def test_user_has_perm(self):
        """Tests that "user_has_perm" check perms on both model and obj levels.
        """            
        u7, n = get_user_model().objects.get_or_create(username="u7")
        u8, n = get_user_model().objects.get_or_create(username="u8")
        
        prev_user = logged_cache.user
        
        # Checking perms for u7 (saved in LoggedInUserCache).
        logged_cache.user = u7
        self.assertFalse(user_has_perm(u8, "%s.view_user" % auth_app))
        self.assertFalse(user_has_perm(u8, "%s.change_user" % auth_app))
        self.assertFalse(user_has_perm(u8, "%s.delete_user" % auth_app))
        
        op, n = ObjectPermission.objects.get_or_create_by_uid("%s.view_user.%s" % (auth_app, u8.pk))
        u7.objectpermissions.add(op)
        
        clear_perm_caches(u7)
    
        self.assertTrue(user_has_perm(u8, "%s.view_user" % auth_app))
        self.assertFalse(user_has_perm(u8, "%s.change_user" % auth_app))
        self.assertFalse(user_has_perm(u8, "%s.delete_user" % auth_app))
        
        p, n = Permission.objects.get_or_create_by_uid("%s.change_user" % auth_app)
        u7.user_permissions.add(p)
        
        clear_perm_caches(u7)
        
        self.assertTrue(user_has_perm(u8, "%s.view_user" % auth_app))
        self.assertTrue(user_has_perm(u8, "%s.change_user" % auth_app))
        self.assertFalse(user_has_perm(u8, "%s.delete_user" % auth_app))
        
        # Restores previous cached user.
        logged_cache.user = prev_user
        
class BreadcrumbsTagsTestCase(TestCase):
    urls = 'djangoerp.core.tests.urls'
    
    def setUp(self):
        self.context = {"request": FakeRequest()}
        self.clear_breadcrumbs()
        
    def del_breadcrumbs(self):
        delattr(self.context['request'], 'breadcrumbs')
        
    def clear_breadcrumbs(self):
        self.context['request'].breadcrumbs = []
        
    def get_breadcrumbs(self):
        return self.context['request'].breadcrumbs
        
    def test_adding_breadcrumbs_var_to_context(self):
        """Tests adding by default "breadcrumbs" var to context if not present.
        """
        self.del_breadcrumbs()
        
        self.assertFalse(hasattr(self.context['request'], 'breadcrumbs'))
        
        add_crumb(self.context, "Go")
        
        self.assertTrue(hasattr(self.context['request'], 'breadcrumbs'))
        self.assertEqual(type(self.context['request'].breadcrumbs), list)
        
        self.clear_breadcrumbs()
        
    def test_fail_adding_empty_crumb(self):
        """Tests empty crumbs are not allowed.
        """
        self.clear_breadcrumbs()
        
        self.assertEqual(len(self.get_breadcrumbs()), 0)
        
        add_crumb(self.context, None)
        
        self.assertEqual(len(self.get_breadcrumbs()), 0)
        
    def test_add_crumb_with_empty_url(self):
        """Tests "add_crumb" templatetag with an empty URL.
        """
        self.clear_breadcrumbs()
        
        self.assertEqual(len(self.get_breadcrumbs()), 0)
        
        add_crumb(self.context, "Home")
        
        self.assertEqual(len(self.get_breadcrumbs()), 1)
        self.assertEqual(self.get_breadcrumbs()[0], ("Home", None))
        
    def test_add_crumb_with_valid_url(self):
        """Tests "add_crumb" templatetag with a valid URL.
        """
        self.clear_breadcrumbs()
        
        self.assertEqual(len(self.get_breadcrumbs()), 0)
        
        add_crumb(self.context, "Home", "/")
        
        self.assertEqual(len(self.get_breadcrumbs()), 1)
        self.assertEqual(self.get_breadcrumbs()[0], ("Home", "/"))
        
    def test_add_crumb_with_view_name(self):
        """Tests "add_crumb" templatetag with a view name instead of an URL.
        """
        self.clear_breadcrumbs()
        
        self.assertEqual(len(self.get_breadcrumbs()), 0)
        
        add_crumb(self.context, "Home", "private_zone_url")
        
        self.assertEqual(len(self.get_breadcrumbs()), 1)
        self.assertEqual(self.get_breadcrumbs()[0], ("Home", "/private/"))
        
    def test_remove_last_crumb_to_empty_list(self):
        """Tests "remove_last_crumb" templatetag from an empty breadcrumb list.
        """
        self.clear_breadcrumbs()
        
        self.assertEqual(len(self.get_breadcrumbs()), 0)
        
        remove_last_crumb(self.context)
        
        self.assertEqual(len(self.get_breadcrumbs()), 0)        
        
    def test_remove_last_crumb(self):
        """Tests "remove_last_crumb" templatetag from a breadcrumb list.
        """
        self.clear_breadcrumbs()
        
        self.assertEqual(len(self.get_breadcrumbs()), 0)
        
        add_crumb(self.context, "Home", "/")
        add_crumb(self.context, "Private zone", "private_zone_url")
        
        self.assertEqual(len(self.get_breadcrumbs()), 2)
        
        remove_last_crumb(self.context)
        
        self.assertEqual(len(self.get_breadcrumbs()), 1)
        self.assertEqual(self.get_breadcrumbs()[0], ("Home", "/"))
        
    def test_render_invalid_breadcrumbs(self):
        """Tests "render_breadcrumbs" templatetag without registered breadcrumbs.
        """
        self.del_breadcrumbs()
        
        self.assertEqual(render_breadcrumbs(self.context), {"breadcrumbs": None})
        
        self.clear_breadcrumbs()
        
    def test_render_empty_breadcrumbs(self):
        """Tests "render_breadcrumbs" templatetag with an empty breadcrumb list.
        """
        self.clear_breadcrumbs()
        
        self.assertEqual(render_breadcrumbs(self.context), {"breadcrumbs": []})
        
    def test_render_breadcrumbs(self):
        """Tests "render_breadcrumbs" templatetag with a valid breadcrumb list.
        """
        self.clear_breadcrumbs()
        
        add_crumb(self.context, "Home", "/")
        add_crumb(self.context, "Private zone", "private_zone_url")
        
        self.assertEqual(
            render_breadcrumbs(self.context),
            {"breadcrumbs": [("Home", "/"), ("Private zone", "/private/")]}
        )
        
class AvatarTagTestCase(TestCase):
    def test_empty_avatar(self):
        """Tests "avatar" templatetag with empty params.
        """
        self.assertEqual(
            avatar(None),
            '<img class="avatar image" width="32" height="32" src="http://www.gravatar.com/avatar/?s=32&r=g&d=mm" />'
        )
        
    def test_valid_avatar(self):
        """Tests "avatar" templatetag with valid email.
        """
        self.assertEqual(
            avatar("u@u.it"),
            '<img class="avatar image" width="32" height="32" src="http://www.gravatar.com/avatar/754331256868501f6cdcc08efab6dd1e?s=32&r=g&d=mm" />'
        )
        
    def test_set_avatar_size(self):
        """Tests "avatar" templatetag with different size.
        """
        self.assertEqual(
            avatar("u@u.it", 80),
            '<img class="avatar image" width="80" height="80" src="http://www.gravatar.com/avatar/754331256868501f6cdcc08efab6dd1e?s=80&r=g&d=mm" />'
        )
        
    def test_set_default_avatar(self):
        """Tests "avatar" templatetag with a default image.
        """
        self.assertEqual(
            avatar("u@u.it", default="http://localhost:8000/my_default_image.jpg"),
            '<img class="avatar image" width="32" height="32" src="http://www.gravatar.com/avatar/754331256868501f6cdcc08efab6dd1e?s=32&r=g&d=http://localhost:8000/my_default_image.jpg" />'
        )
