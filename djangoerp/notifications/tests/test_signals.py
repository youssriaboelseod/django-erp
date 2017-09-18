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
from django.db import models

from ..signals import *

class MakeObservableTestCase(TestCase):
    def test_apply_make_observable(self):
        """Tests appy mixin.
        """
        class TestModel1(models.Model):
            pass

        m = TestModel1()

        self.assertFalse(isinstance(m, Observable))
        self.assertFalse(models.signals.pre_delete.has_listeners(TestModel1))
        self.assertFalse(models.signals.post_save.has_listeners(TestModel1))

        make_observable(m)

        self.assertTrue(isinstance(m, Observable))
        self.assertTrue(models.signals.pre_delete.has_listeners(TestModel1))
        self.assertTrue(models.signals.post_save.has_listeners(TestModel1))

        self.assertTrue('modified' in m._Observable__change_exclude)
        self.assertEqual(
            m._Observable__subscriber_fields, 
            ['parent', 'owner', 'author', 'created_by']
        )

class MakeDefaultNotifierTestCase(TestCase):
    def test_apply_make_default_notifier(self):
        """Tests appy mixin.
        """
        class TestModel2(models.Model):
            pass

        m = TestModel2()

        self.assertFalse(isinstance(m, Observable))
        self.assertFalse(models.signals.post_save.has_listeners(TestModel2))
        self.assertFalse(post_change.has_listeners(TestModel2))
        self.assertFalse(models.signals.m2m_changed.has_listeners(TestModel2))
        self.assertFalse(models.signals.post_delete.has_listeners(TestModel2))

        make_default_notifier(m)
        
        self.assertTrue(isinstance(m, Observable))
        self.assertTrue(models.signals.post_save.has_listeners(TestModel2))
        self.assertTrue(post_change.has_listeners(TestModel2))
        self.assertTrue(models.signals.m2m_changed.has_listeners(TestModel2))
        self.assertTrue(models.signals.post_delete.has_listeners(TestModel2))

class MakeNotificationTargetTestCase(TestCase):
    def test_apply_make_notification_target(self):
        """Tests appy mixin.
        """
        class TestModel3(models.Model):
            pass

        m = TestModel3()

        self.assertFalse(isinstance(m, NotificationTarget))

        make_notification_target(m)

        self.assertTrue(isinstance(m, NotificationTarget))
        
