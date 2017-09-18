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


from django.conf.urls import url, include
from django.conf import settings
from django.apps import apps as app_registry


urlpatterns = []


def has_urls(app):
    if app:
        try:
            return getattr(app, 'urls', None) or  __import__("%s.urls" % app.name, {}, {}, ["*"])
        except ImportError:
            pass
    return False


# Basic URL patterns bootstrap.
if 'django.contrib.admin' in settings.INSTALLED_APPS:
    if 'django.contrib.admindocs' in settings.INSTALLED_APPS:
        urlpatterns += [
            url(r'^admin/doc/', include('django.contrib.admindocs.urls'))
        ]
    from django.contrib import admin
    admin.autodiscover()
    urlpatterns += [
        url(r'^admin/', include(admin.site.urls))
    ]

if 'django.contrib.staticfiles' in settings.INSTALLED_APPS:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()


urlpatterns += [url(r'^', include('%s.urls' % app.name)) for app in app_registry.get_app_configs() if has_urls(app)]
