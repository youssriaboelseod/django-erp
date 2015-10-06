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


from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.db.models import permalink
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from djangoerp.core.models import validate_json


@python_2_unicode_compatible
class Menu(models.Model):
    """Menu model.
    """
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_('slug'))
    description = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('description'))
    template_name = models.CharField(max_length=255, blank=True, verbose_name=_('template name'))

    class Meta:
        verbose_name = _('menu')
        verbose_name_plural = _('menus')

    def __str__(self):
        return self.description or self.slug


@python_2_unicode_compatible
class Link(models.Model):
    """A generic menu entry.
    """
    menu = models.ForeignKey(Menu, related_name='links', verbose_name=_('menu'))
    title = models.CharField(max_length=255, verbose_name=_('title'))
    slug = models.SlugField(unique=True, verbose_name=_('slug'))
    url = models.CharField(max_length=255, verbose_name=_('url'))
    icon = models.CharField(max_length=100, blank=True, verbose_name=_('icon'))
    template_name = models.CharField(max_length=255, blank=True, verbose_name=_('template name'))
    context = models.TextField(blank=True, null=True, validators=[validate_json], help_text=_('Use the JSON syntax.'), verbose_name=_('context'))
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('description'))
    new_window = models.BooleanField(default=False, verbose_name=_('New window'))
    sort_order = models.PositiveIntegerField(default=0, verbose_name=_('sort order'))
    submenu = models.ForeignKey(Menu, db_column='submenu_id', related_name='parent_links', blank=True, null=True, verbose_name=_('sub-menu'))
    only_authenticated = models.BooleanField(default=True, verbose_name=_('Only for authenticated users'))
    only_staff = models.BooleanField(default=False, verbose_name=_('Only for staff users'))
    only_with_perms = models.ManyToManyField(Permission, blank=True, verbose_name=_('Only with following permissions'))

    class Meta:
        ordering = ('menu', 'sort_order', 'id',)
        verbose_name = _('link')
        verbose_name_plural = _('links')
        
    def __init__(self, *args, **kwargs):
        self.extra_context = kwargs.pop("extra_context", {})
        super(Link, self).__init__(*args, **kwargs)

    def __str__(self):
        return '%s | %s' % (self.menu, self.get_title())

    def get_absolute_url(self):
        import json
        from django.template import Variable
        from django.core.urlresolvers import reverse, NoReverseMatch
        
        link_context = {}
        
        for k, v in json.loads(self.context or "{}").items():
            value = v
            try:
                v = Variable(v).resolve(self.extra_context)
            except:
                pass
            link_context[k] = v
            
        absolute_url = self.url % self.extra_context
        
        try:
            absolute_url = reverse(absolute_url, args=[], kwargs=link_context)
        except NoReverseMatch:
            pass
            
        return absolute_url

    def get_title(self):
        return self.title % self.extra_context

    def get_description(self):
        return self.description % self.extra_context

    def get_template_name(self):
        return self.template_name % self.extra_context

    def get_icon(self):
        return self.icon % self.extra_context


@python_2_unicode_compatible
class Bookmark(Link):
    """A proxy model for bookmark links.
    """
    class Meta:
        proxy = True
        verbose_name = _('bookmark')
        verbose_name_plural = _('bookmarks')

    def __str__(self):
        return '%s' % (self.title % self.extra_context)
        
    @models.permalink
    def get_edit_url(self):
        return ('bookmark_edit', (), {"slug": self.slug})

    @models.permalink
    def get_delete_url(self):
        return ('bookmark_delete', (), {"slug": self.slug})
