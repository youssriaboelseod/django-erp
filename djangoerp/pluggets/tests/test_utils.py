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
__version__ = '0.0.4'

from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Region
from ..utils import *
          
class UtilsTestCase(TestCase):
    def test_dashboard_for_user(self):
        """Tests retrieving the dashboard owned by user with a given username.
        """        
        u1, n = get_user_model().objects.get_or_create(username="u1")
        
        self.assertTrue(n)
        
        dashboard = Region.objects.get(slug="user_1_dashboard")
        
        self.assertEqual(get_dashboard_for(u1.username), dashboard)
        
    def test_user_of_dashboard(self):
        """Tests retrieving the user of dashboard identified by the given slug.
        """        
        u1, n = get_user_model().objects.get_or_create(username="u1")
        dashboard = Region.objects.get(slug="user_1_dashboard")
        
        self.assertEqual(get_user_of(dashboard.slug), u1)
