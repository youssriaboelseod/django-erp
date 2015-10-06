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

from django.contrib.auth import get_user_model

from .models import Menu

def get_bookmarks_slug_for(instance):
    """Returns the slug for a bookmark menu valid for the given model instance.
    """
    kls = instance.__class__
    return "%s_%d_bookmarks" % (kls.__name__.lower(), instance.pk)

def create_bookmarks(instance):
    """Creates a new bookmarks list for the given object.
    """            
    from djangoerp.core.cache import LoggedInUserCache
            
    logged_cache = LoggedInUserCache()
    current_user = logged_cache.user
    
    if isinstance(instance, get_user_model()):
        logged_cache.user = instance
        
    kls = instance.__class__
            
    bookmarks, is_new = Menu.objects.get_or_create(slug=get_bookmarks_slug_for(instance), description="Bookmarks for %s:%s" % (kls.__name__, instance.pk))
            
    logged_cache.user = current_user
    
    return bookmarks, is_new

def delete_bookmarks(instance):
    """Deletes the bookmarks list of the given object.
    """
    try:
        bookmarks = Menu.objects.get(slug=get_bookmarks_slug_for(instance))
        bookmarks.delete()
    except Menu.DoesNotExist:
        pass

def get_bookmarks_for(username):
    """Returns the bookmarks menu for the user with the given username.
    """
    user = get_user_model().objects.get(username=username)
    return Menu.objects.get(slug=get_bookmarks_slug_for(user))
    
def get_user_of(bookmarks_menu_slug):
    """Returns the owner of the given bookmarks list.
    """
    user_pk = bookmarks_menu_slug.split('_')[1]
    return get_user_model().objects.get(pk=user_pk)
    
def create_detail_navigation(cls):
    """Create a navigation menu for the detail view of the given model class.
    
    This function could be used to automatically create a list of navigation
    links (tabs) to be used in the given model class detail view.
    """
    cls_name = cls.__name__.lower()
    return Menu.objects.get_or_create(slug="%s_detail_navigation" % (cls_name), description="%s navigation" % (cls_name.capitalize()))
    
def create_detail_actions(cls):
    """Create an action menu for the detail view of the given model class.
    
    This function could be used to automatically create a list of action
    links to be used in the given model class detail view.
    """
    cls_name = cls.__name__.lower()
    return Menu.objects.get_or_create(slug="%s_detail_actions" % (cls_name), description="%s actions" % (cls_name.capitalize()))
    
def create_list_actions(cls):
    """Create an action menu for the list view of the given model class.
    
    This function could be used to automatically create a list of action
    links to be used in the given model class list view.
    """
    cls_name = cls.__name__.lower()
    return Menu.objects.get_or_create(slug="%s_list_actions" % (cls_name), description="%s list actions" % (cls_name.capitalize()))
