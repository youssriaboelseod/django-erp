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
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from ..models import *

class FollowRelationTestCase(TestCase):
    def test_unicode_representation(self):
        """Tests unicode representation.
        """
        user_model = get_user_model()
        
        u1 = user_model.objects.create(username="u1")
        u2 = user_model.objects.create(username="u2")
        fr = FollowRelation.objects.create(followed=u2, follower=u1)
        
        self.assertEqual("%s" % fr, "%s followed by %s" % (u2, u1))

class SignatureTestCase(TestCase):
    def test_unicode_representation(self):
        """Tests unicode representation.
        """
        title = "Create a generic object"
        s = Signature.objects.create(slug="create_object", title=title)
        
        self.assertEqual("%s" % s, title)
        
    def test_generate_title_on_save(self):
        """Tests automatic title generation on save.
        """
        s = Signature.objects.create(slug="edit_object")
        
        self.assertEqual(s.title, "Edit object")

class SubscriptionTestCase(TestCase):
    def test_unicode_representation(self):
        """Tests unicode representation.
        """
        user_model = get_user_model()
        
        u1 = user_model.objects.create(username="u1")
        s = Signature.objects.create(slug="object-changed")
        sub = Subscription.objects.create(subscriber=u1, signature=s)
        
        self.assertEqual("%s" % sub, "%s | %s" % (u1, s))

class ActivityTestCase(TestCase):
    def setUp(self):
        user_model = get_user_model()
        
        self.u1 = user_model.objects.create(username="u1")
        self.signature = "object-changed"
        
    def test_unicode_representation(self):
        """Tests unicode representation.
        """
        a1 = Activity.objects.create(title="New activity %(name)s 1", source=self.u1, signature=self.signature)
        
        self.assertEqual("%s" % a1, "New activity %(name)s 1")
        
        a1.context = '{"name": "with name"}'
        
        self.assertEqual("%s" % a1, "New activity with name 1")
        
    def test_get_context(self):
        """Tests "get_context" method.
        """
        a2 = Activity.objects.create(title="Activity 2", source=self.u1, signature=self.signature)
        
        self.assertEqual(a2.get_context(), {})
        
        a2.context = '{"name": "with name"}'
        
        self.assertEqual(a2.get_context(), {"name": "with name"})
        
    def test_get_template_name(self):
        """Tests "get_template_name" method.
        """
        a3 = Activity.objects.create(title="Activity 3", source=self.u1, signature=self.signature)
        
        self.assertEqual(a3.get_template_name(), "notifications/activities/%s.html" % self.signature)
        
        a3.template = "notifications/activities/index.html"
        
        self.assertEqual(a3.get_template_name(), "notifications/activities/index.html")
        
    def test_get_content(self):
        """Tests "get_content" method.
        """
        from django.template.loader import render_to_string
        
        a4 = Activity.objects.create(title="Activity 4", source=self.u1, signature=self.signature)
        
        self.assertEqual(a4.get_content(), render_to_string("notifications/activities/object-changed.html", a4.get_context()))
        
        a4.template = "notifications/activities/index.html"
        
        self.assertEqual(a4.get_content(), "")
        
    def test_get_absolute_url(self):
        """Tests "get_absolute_url" method.
        """
        a5 = Activity.objects.create(title="Activity 5", source=self.u1, signature=self.signature)
        
        self.assertEqual(a5.get_absolute_url(), "")
        
        a5.backlink = self.u1.get_absolute_url()
        
        self.assertEqual(a5.get_absolute_url(), self.u1.get_absolute_url())

class NotificationTestCase(TestCase):
    def setUp(self):
        user_model = get_user_model()
        
        self.u1 = user_model.objects.create(username="u1")
        self.signature = Signature.objects.create(slug="object-changed")
        self.n1 = Notification.objects.create(title="Notification 1", target=self.u1, signature=self.signature)
        
    def test_unicode_representation(self):
        """Tests unicode representation.
        """
        self.assertEqual("%s" % self.n1, "Notification 1")
        
    def test_get_urls(self):
        """Tests "get_*_url" methods.
        """        
        self.assertEqual(self.n1.get_absolute_url(), "/users/%s/notifications/%s/" % (self.u1.pk, self.n1.pk))        
        self.assertEqual(self.n1.get_delete_url(), "/users/%s/notifications/%s/delete/" % (self.u1.pk, self.n1.pk))
        
    def test_clean_dispatch_uid(self):
        """Tests auto-generation of "dispatch_uid" value.
        """
        self.assertNotEqual(self.n1.dispatch_uid, "")
        
    def test_clean_subscription(self):
        """Tests checking of a valid subscription of target for given signature.
        """
        """
        s = Signature.objects.create(slug="another-object-activity-signature")
        
        self.assertEqual(Subscription.objects.filter(subscriber=self.u1, signature=s).count(), 0)
        
        create_func = lambda : Notification.objects.create(title="Invalid", target=self.u1, signature=s)
        
        self.assertRaises(ValidationError, create_func)"""
        
class ObservableTestCase(TestCase):
    def setUp(self):
        user_model = get_user_model()
        
        self.u1 = user_model.objects.create(username="u1")
        if not isinstance(self.u1, Observable):
            self.u1.cls.__bases__ += (Observable,)
            
    def test_caching_changes(self):
        """Tests caching changes to instnace's attributes.
        """
        self.u1.username = "u1"
        self.u1._Observable__changes = {}
        
        self.u1.username = "u2"
        self.assertEqual(self.u1._Observable__changes, {"username": ("u1", "u2")})
        
        self.u1.username = "u3"
        self.assertEqual(self.u1._Observable__changes, {"username": ("u1", "u3")})
        
    def test_followers(self):
        """Tests following logic.
        """
        self.u1.add_followers(self.u1)
        
        self.assertEqual(self.u1.followers(), [self.u1])
        
        self.u1._Observable__followers_cache = [1]
        
        self.assertEqual(self.u1.followers(), [1])
        
        self.u1._Observable__followers_cache = None
        
        self.u1.remove_followers(self.u1)
        
        self.assertEqual(self.u1.followers(), [])
        
class NotificationTargetTestCase(TestCase):
    def setUp(self):
        user_model = get_user_model()
        
        self.u1 = user_model.objects.create(username="u1")
        if not isinstance(self.u1, NotificationTarget):
            self.u1.cls.__bases__ += (NotificationTarget,)
            
        self.signature = Signature.objects.create(slug="object-changed")
            
    def test_notification_set(self):
        """Tests "notification_set" read-only property.
        """
        n1 = Notification.objects.create(title="Notification 1", target=self.u1, signature=self.signature)
        n2 = Notification.objects.create(title="Notification 2", target=self.u1, signature=self.signature)
        
        self.assertQuerysetEqual(
            self.u1.notification_set,
            [repr(n1), repr(n2)],
            ordered=False
        )
