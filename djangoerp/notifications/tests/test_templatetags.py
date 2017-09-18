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
from django.utils.timezone import now
from django.contrib.auth import get_user_model

from ..models import *
from ..templatetags.notifications import *

class NotificationForTagTestCase(TestCase):
    def test_templatetag(self):
        """Tests defualt behavior.
        """
        u1 = get_user_model().objects.create(username="u1")
        u2 = get_user_model().objects.create(username="u2")
        
        self.assertQuerysetEqual(
            notification_for(u1),
            [],
            ordered=False
        ) 
        
        self.assertQuerysetEqual(
            notification_for(u2),
            [],
            ordered=False
        )
        
        signature = Signature.objects.create(slug="test-notification")
        
        n1 = Notification.objects.create(
            title="Test!",
            signature=signature,
            target=u1
        )
        
        n2 = Notification.objects.create(
            title="Test!",
            signature=signature,
            target=u1,
            read=now()
        )
        
        n3 = Notification.objects.create(
            title="Test!",
            signature=signature,
            target=u2
        )
        
        self.assertQuerysetEqual(
            notification_for(u1),
            [repr(n1), repr(n2)],
            ordered=False
        ) 
        
        self.assertQuerysetEqual(
            notification_for(u2),
            [repr(n3)],
            ordered=False
        )

class UnreadNotificationForTagTestCase(TestCase):
    def test_templatetag(self):
        """Tests defualt behavior.
        """
        u1 = get_user_model().objects.create(username="u1")
        u2 = get_user_model().objects.create(username="u2")
        
        self.assertQuerysetEqual(
            notification_for(u1),
            [],
            ordered=False
        ) 
        
        self.assertQuerysetEqual(
            notification_for(u2),
            [],
            ordered=False
        )
        
        signature = Signature.objects.create(slug="test-notification")
        
        n1 = Notification.objects.create(
            title="Test!",
            signature=signature,
            target=u1
        )
        
        n2 = Notification.objects.create(
            title="Test!",
            signature=signature,
            target=u1,
            read=now()
        )
        
        n3 = Notification.objects.create(
            title="Test!",
            signature=signature,
            target=u2
        )
        
        self.assertQuerysetEqual(
            unread_notification_for(u1),
            [repr(n1)],
            ordered=False
        ) 
        
        self.assertQuerysetEqual(
            unread_notification_for(u2),
            [repr(n3)],
            ordered=False
        )
