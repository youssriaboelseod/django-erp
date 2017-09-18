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

from . import *
from ..models import Region, Plugget
from ..utils import get_dashboard_for
from ..signals import *
       
class SignalTestCase(TestCase):
    def test_dashboard_auto_creation_for_users(self):
        """Tests a dashboard must be auto-created for new users.
        """
        self.assertEqual(Region.objects.filter(slug="user_1_dashboard").count(), 0)
        
        u1, n = get_user_model().objects.get_or_create(username="u1")
        
        self.assertTrue(n)
        self.assertEqual(Region.objects.filter(slug="user_1_dashboard").count(), 1)
        
    def test_manage_author_permissions_on_dashboard(self):
        """Tests that "manage_author_permissions" auto-generate perms for author. 
        """        
        u1, n = get_user_model().objects.get_or_create(username="u1")
        dashboard = get_dashboard_for(u1.username)
        
        self.assertTrue(ob.has_perm(u1, "pluggets.view_region", dashboard))
        self.assertTrue(ob.has_perm(u1, "pluggets.change_region", dashboard))
        self.assertTrue(ob.has_perm(u1, "pluggets.delete_region", dashboard))        
        
    def test_manage_author_permissions_on_plugget(self):
        """Tests that "manage_author_permissions" auto-generate perms for author. 
        """
        u2, n = get_user_model().objects.get_or_create(username="u2")
        u3, n = get_user_model().objects.get_or_create(username="u3")
        
        prev_user = logged_cache.user
        
        # The current author ("logged" user) is now u2.
        logged_cache.user = u2
        
        p1, n = Plugget.objects.get_or_create(region=get_dashboard_for(u2.username), title="p1", source="djangoerp.pluggets.base.dummy", template="pluggets/base_plugget.html")
        
        self.assertTrue(ob.has_perm(u2, "pluggets.view_plugget", p1))
        self.assertTrue(ob.has_perm(u2, "pluggets.change_plugget", p1))
        self.assertTrue(ob.has_perm(u2, "pluggets.delete_plugget", p1))
        
        self.assertFalse(ob.has_perm(u3, "pluggets.view_plugget", p1))
        self.assertFalse(ob.has_perm(u3, "pluggets.change_plugget", p1))
        self.assertFalse(ob.has_perm(u3, "pluggets.delete_plugget", p1))
        
        # Restores previous cached user.
        logged_cache.user = prev_user
        
    def test_dashboard_auto_deletion(self):
        """Tests automatic deletion of dashboards when their owners are deleted.
        """
        d = None
        
        try:
            d = get_dashboard_for("u4")
        except:
            pass
            
        self.assertEqual(d, None)
            
        u4, n = get_user_model().objects.get_or_create(username="u4")
        
        try:
            d = get_dashboard_for("u4")
        except:
            pass
            
        self.assertNotEqual(d, None)
        
        u4.delete()
        
        try:
            d = get_dashboard_for("u4")
        except:
            d = None
            
        self.assertEqual(d, None)
        
    def test_dashboard_auto_deletion_fails_silently(self):
        """Tests silent failure of deletion when no dashboard is attached.
        """            
        u5, n = get_user_model().objects.get_or_create(username="u5")
        d = get_dashboard_for("u5")
        d.delete()
        
        self.assertRaises(Region.DoesNotExist, lambda: get_dashboard_for(u5.username))
        
        u5.delete()
        
