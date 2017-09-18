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


from django.utils.translation import ugettext_noop as _
from djangoerp.menus.utils import get_bookmarks_for
from djangoerp.menus.models import Menu

from .loading import registry
from .forms import TextPluggetForm


def dummy(context):
    return registry.default_func(context)

def menu(context):
    """Menu plugget.
    
    Simply renders a menu.
    """
    """
    It adds a context variables:
    
     * name -- Slug of selected menu.
    """
    pk = None
    if "menu_id" in context:
        # NOTE: Here, "context" is not a simple dict instance, so we can't use:
        #
        #       >> pk = context.pop("menu_id", None)
        #
        pk = context.get('menu_id')
        del context['menu_id']
    if pk:
        menu = Menu.objects.get(pk=pk)
        context["name"] = menu.slug
    return context
    
def bookmarks_menu(context):
    """Bookmarks plugget.
    
    Shows all your bookmarks.
    """
    if 'user' in context:
        context['menu_id'] = get_bookmarks_for(context['user'].username).pk  
    return menu(context)
        
registry.register_simple_plugget_source(_("Text plugget"),  _("Simply renders a text paragraph."), form=TextPluggetForm)
