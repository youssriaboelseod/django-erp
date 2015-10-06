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
from django.contrib.auth import get_user_model

from ..models import Region
from ..utils import *
          
class DashboardForUserUtilTestCase(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        
    def test_dashboard_for_user(self):
        """Tests retrieving the dashboard owned by user with a given username.
        """        
        u1, n = self.user_model.objects.get_or_create(username="u1")
        
        self.assertTrue(n)
        
        dashboard = Region.objects.get(slug="user_1_dashboard")
        
        self.assertEqual(get_dashboard_for(u1.username), dashboard)
        
    def test_raise_error_on_invalid_username(self):
        """Tests raising an error when an invalid username is given.
        """        
        self.assertRaises(Region.DoesNotExist, lambda : get_dashboard_for("u2"))

class UserOfDashboardUtilTestCase(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        
    def test_user_of_dashboard(self):
        """Tests retrieving the user of dashboard identified by the given slug.
        """        
        u1, n = self.user_model.objects.get_or_create(username="u1")
        dashboard = Region.objects.get(slug="user_1_dashboard")
        
        self.assertEqual(get_user_of(dashboard.slug), u1)
        
    def test_raise_error_on_invalid_dashboard(self):
        """Tests raising an error when an invalid dashboard slug is given.
        """
        self.assertRaises(self.user_model.DoesNotExist, lambda : get_user_of("user_2_dashboard"))
