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


from django.apps import apps as app_registry
from .dependencies import check_dependency


class AppConfigMixin(object):
    dependencies = []
    signals = None
    urls = None

    def __init__(self, *args, **kwargs):
        self.check_dependencies()
        if self.name and not args:
            parent_package, sep, module_name = self.name.rpartition('.')
            if 'app_name' not in kwargs:
                kwargs['app_name'] = self.name
            if 'app_module' not in kwargs:
                kwargs['app_module'] = __import__(self.name, fromlist=[parent_package])
        super(AppConfigMixin, self).__init__(*args, **kwargs)

    def check_dependencies(self):
        for d in self.dependencies:
            check_dependency(d)

    def ready(self):
        self.urls = __import__("%s.urls" % self.name, {}, {}, ["*"])

        try:
            self.signals = __import__("%s.signals" % self.name, {}, {}, ["*"])
        except ImportError:
            pass
