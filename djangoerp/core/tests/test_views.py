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
from django.test.utils import override_settings

from ..models import User
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
