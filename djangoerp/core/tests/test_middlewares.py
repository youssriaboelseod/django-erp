#!/usr/bin/env python
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
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test.utils import override_settings

from . import *
from ..middleware import *
        

@override_settings(ROOT_URLCONF='djangoerp.core.tests.urls')
class RequireLoginMiddlewareTestCase(TestCase):
    
    def test_required_url(self):
        """Tests an URL in required list must be accessible only after a login.
        """
        from django.conf import settings

        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith("%s?next=/" % settings.LOGIN_URL))
        
    def test_exception_url(self):
        """Tests an URL in exception list must be accessible without logging in.
        """
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, 200)
    
    @override_settings(LOGIN_REQUIRED_URLS=(r'/private/(.*)$',))      
    def test_url_without_match(self):
        """Tests no specifi handling for URL without a match.
        """
        response = self.client.get('/private/')
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)       
    
class LoggedInUserCacheMiddlewareTestCase(TestCase):
    def test_store_request_user(self):
        """Tests the correct storing of the current user in the logged cache.
        """
        def get_response(request):
            request.logged_in_user = logged_cache.user
            request.has_user = logged_cache.has_user

        r = FakeRequest()
        m = LoggedInUserCacheMiddleware(get_response)
        u, n = get_user_model().objects.get_or_create(username="u1")
        m(r)
        
        self.assertTrue(isinstance(r.logged_in_user, AnonymousUser))
        self.assertFalse(r.has_user)
        
        r.user = u
        m(r)
        
        self.assertEqual(r.logged_in_user, u)
        self.assertTrue(r.has_user)
        
        logged_cache.clear()
