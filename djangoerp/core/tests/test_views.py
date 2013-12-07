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
