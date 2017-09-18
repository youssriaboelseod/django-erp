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


import re
from django import template
from django.conf import settings
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from ..models import Menu


register = template.Library()


def _calculate_link_params(link, context):
    """Helper function to prepare a link for rendering.

    It takes a link instance, a context and calculates the final values
    of its params (i.e. URL, title, description, etc.)
    """
    user = context.get('user', None)
    link.extra_context = context
    link.title = link.title % context
    if link.description:
        link.description = link.description % context
    perms = ["%s.%s" % (p.content_type.app_label, p.codename) for p in link.only_with_perms.all()]
    link.authorized = True
    if isinstance(user, get_user_model()) and not user.is_superuser:
        if link.only_staff and not (user.is_staff or user.is_superuser):
            link.authorized = False
        if link.only_with_perms.exists() and not user.has_perms(perms, context.get("object", None)):
            link.authorized = False
    elif not user or isinstance(user, AnonymousUser):
        user = AnonymousUser()
        if link.only_staff or link.only_with_perms.exists():
            link.authorized = False
        if link.only_authenticated and not user.is_authenticated():
            link.authorized = False
    return link
    

def _render_menu(slug, context, html_template=None, css_class=None):
    """Helper function to render a maneu.

    It takes a menu slug, a context, a template name, any CSS class and
    renders the given menu using the given attributes.
    """
    try:
        links = None
        if isinstance(slug, template.Variable):
            slug = slug.resolve(context)
        if isinstance(html_template, template.Variable):
           html_template = html_template.resolve(context)
        if isinstance(css_class, template.Variable):
           css_class = css_class.resolve(context)
        menu = Menu.objects.get(slug=slug)
        links = menu.links.all()
        for link in links:
            _calculate_link_params(link, context)
        html_template = html_template or menu.template_name or settings.MENU_DEFAULT_TEMPLATE
        html_template = ("%s" % html_template).replace('"', '').replace("'", "")
        return render_to_string(html_template, {'slug': slug, 'links': links, 'css_class': css_class}, context)
    except Menu.DoesNotExist:
        pass
    return ""


@register.simple_tag(takes_context=True)
def render_menu(context, slug, html_template=None, css_class=None):
    """Renders a menu.

    Example tag usage: {% render_menu menu_slug [html_template] [css_class] %}
    """
    return _render_menu(slug, context, html_template, css_class)
    

@register.simple_tag(takes_context=True)
def render_user_bookmarks(context, css_class=None):
    """Renders the bookmark menu for the current logged user.
    
    Example tag usage: {% render_user_bookmarks [css_class] %}
    """
    user = context.get('user', None)
    if isinstance(user, get_user_model()) and user.pk:
        return _render_menu("user_%d_bookmarks" % user.pk, context, None, css_class)
    return ""    


@register.assignment_tag(takes_context=True)
def score_link(context, link, ref_url, css_class="active"):
    """Checks if the link instance is the best match for "ref_url".

    Example tag usage: {% score_link link ref_url [css_class] as class %}
    """
    def best_match(menu, parent=None, score=len(ref_url), matched_link=None):
        if menu:
            for l in menu.links.all():
                l = _calculate_link_params(l, context)
                url = l.get_absolute_url()
                if url == ref_url or ref_url.startswith(url):
                    remainder = ref_url[len(url):]
                    current_score = len(remainder)
                    if current_score < score:
                        score = current_score
                        matched_link = parent or l
                        continue
                score, matched_link = best_match(l.submenu, parent or l, score, matched_link)
        return score, matched_link
    score, matched_link = best_match(link.menu)                              
    if matched_link == link:
        return css_class
    return ""
