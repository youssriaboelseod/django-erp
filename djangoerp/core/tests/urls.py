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


from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from ..urls import urlpatterns
from ..views import SetCancelUrlMixin


class BaseTemplateView(TemplateView):
    template_name = "index.html"

class SetCancelUrlTestView(SetCancelUrlMixin, BaseTemplateView):
    pass

class PresetSetCancelUrlTestView(SetCancelUrlTestView):
    cancel_url = "/go_to_cancel_url/"

# Special urls for test cases.
urlpatterns += patterns('',
    url(r'^default_cancel_url/', view=SetCancelUrlTestView.as_view(), name="default_cancel_url"),
    url(r'^preset_cancel_url/', view=PresetSetCancelUrlTestView.as_view(), name="preset_cancel_url"),
    url(r'^private/', view=BaseTemplateView.as_view(), name="private_zone_url"),
)

