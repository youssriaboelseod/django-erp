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

from ..models import Region, Plugget


class AppConfigTestCase(TestCase):
    def test_initial_fixture_installation(self):
        """Tests installation of initial fixture.
        """
        from djangoerp.core.models import Group
        
        # Regions.
        footer_region, is_new = Region.objects.get_or_create(slug="footer")
        self.assertTrue(footer_region)
        self.assertFalse(is_new)
        
        sidebar_region, is_new = Region.objects.get_or_create(slug="sidebar")
        self.assertTrue(sidebar_region)
        self.assertFalse(is_new)
        
        # Pluggets.
        main_menu_plugget, is_new = Plugget.objects.get_or_create(title="Main menu")
        self.assertTrue(main_menu_plugget)
        self.assertFalse(is_new)
        
        powered_by_plugget, is_new = Plugget.objects.get_or_create(title="Powered by")
        self.assertTrue(powered_by_plugget)
        self.assertFalse(is_new)
        
        # Perms.
        users_group, is_new = Group.objects.get_or_create(name="users")

        self.assertTrue(users_group.permissions.get_by_natural_key("add_plugget", "pluggets", "plugget"))
