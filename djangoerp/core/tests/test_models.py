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

from ..models import *


class JSONValidationCase(TestCase):
    def test_correct_json_validation(self):
        """Tests that when a JSON snippet is incorrect, an error must be raised.
        """
        try:
            validate_json('{"id":1,"name":"foo","interest":["django","django ERP"]}')
            self.assertTrue(True)
        except ValidationError:
            self.assertFalse(True)
          
    def test_incorrect_json_validation(self):
        """Tests that when a JSON snippet is incorrect, an error must be raised.
        """
        try:
            # The snippet is incorrect due to the double closed square bracket.
            validate_json('{"id":1,"name":"foo","interest":["django","django ERP"]]}')
            self.assertFalse(True)
        except ValidationError:
            self.assertTrue(True)
            
class UserModelTestCase(TestCase):
    def test_get_short_name(self):
        """Tests the username must be returned as short name.
        """
        u1, n = User.objects.get_or_create(username="u1")
        
        self.assertEqual(u1.get_short_name(), "u1")

    def test_get_full_name(self):
        """Tests the full name must be equal to the short name.
        """
        u1, n = User.objects.get_or_create(username="u1")
        
        self.assertEqual(u1.get_full_name(), u1.get_short_name())
        
    def test_send_email(self):
        """Tests sending an email to the given user.
        """
        from django.core import mail
        
        u1, n = User.objects.get_or_create(username="u1")
        
        u1.email_user('Subject here', 'Here is the message.', 'from@example.com')
        
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject here')
        self.assertEqual(mail.outbox[0].from_email, 'from@example.com')
        
class GroupModelTestCase(TestCase):
    def test_unicode(self):
        """Tests getting correct unicode representation.
        """
        g, n = Group.objects.get_or_create(name="users")
        
        self.assertEqual("%s" % g, "users")
        
class ObjectPermissionModelTestCase(TestCase):
    def test_unicode(self):
        """Tests getting correct unicode representation.
        """
        u1, n = User.objects.get_or_create(username="u1")
        p, n = ObjectPermission.objects.get_or_create_by_natural_key("view_user", "core", "user", u1.pk)
        
        self.assertEqual("%s" % p, "core | user | Can view user | %d" % u1.pk)
