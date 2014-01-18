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
__copyright__ = 'Copyright (c) 2013-2014, django ERP Team'
__version__ = '0.0.5'

from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import *
from ..views import *

# Not in public API.
from ..views import _get_content_type_by, _get_object_by, \
                    _get_object_view_perm, _get_object, _get_notification
                    
class FakeRequest(object):
    pass

class GetterFunctionsTestCase(TestCase):
    def setUp(self):
        self.request = FakeRequest()
        self.request.user, n = get_user_model().objects.get_or_create(username="u")
        
    def test__get_content_type_by_model_name(self):
        """Tests "_get_content_type_by" function.
        """
        user_model = get_user_model()
        
        self.assertEqual(_get_content_type_by("user").model_class(), user_model)
        self.assertEqual(_get_content_type_by("users").model_class(), user_model)
        
        class User(user_model):
            class Meta:
                proxy = True
        
        self.assertEqual(_get_content_type_by("user").model_class(), user_model)
        self.assertEqual(_get_content_type_by("users").model_class(), user_model)
        
    def test_get_object_by_name_and_id(self):
        """Tests "_get_object_by" function.
        """
        user_model = get_user_model()
        
        self.assertEqual(_get_object_by("user", self.request.user.pk), self.request.user)
        
    def test_get_object_view_perm(self):
        """Tests "_get_object_view_perm" function.
        """
        self.assertEqual(_get_object_view_perm(self.request, object_model="user"), "core.view_user")
        
    def test_get_object(self):
        """Tests "_get_object" function.
        """
        self.assertEqual(_get_object(self.request, object_model="user", object_id=self.request.user.pk), self.request.user)
        
    def test_get_notification(self):
        """Tests "_get_notification" function.
        """
        s, n = Signature.objects.get_or_create(slug="custom.signature")
        nt, n = Notification.objects.get_or_create(title="Test", target=self.request.user, signature=s)
        
        self.assertEqual(_get_notification(self.request, pk=nt.pk), nt)
        
