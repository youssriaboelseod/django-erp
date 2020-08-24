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


from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from .views import *


urlpatterns = [

    # User authentication management.
    url(r'^users/login/$', auth_views.LoginView.as_view(template_name='auth/login.html'), name='user_login'),
    url(r'^users/logout/$', auth_views.logout_then_login, name='user_logout'),
    url(r'^users/(?P<pk>\d+)/$', DetailUserView.as_view(), name='user_detail'),
    url(r'^users/(?P<pk>\d+)/edit/$', UpdateUserView.as_view(), name='user_edit'),
    url(r'^users/(?P<pk>\d+)/delete/$', DeleteUserView.as_view(), name='user_delete'),
    
    # Homepage.
    url(r'^$', TemplateView.as_view(template_name="index.html")),
]
