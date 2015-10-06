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
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext_lazy as _
from djangoerp.core.models import validate_json


@python_2_unicode_compatible
class Region(models.Model):
    """A logical area that could host any kind of Pluggets.
    
    A region could have a 1-1 relation with a specific object (i.e. dashboards).
    """
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_('slug'))
    title = models.CharField(max_length=256, blank=True, null=True, verbose_name=_('title'))
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    owner_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _('region')
        verbose_name_plural = _('regions')

    def __str__(self):
        return self.title or self.slug

    def get_absolute_url(self):
        try:
            from django.contrib.auth import get_user_model
            if not isinstance(self.owner_object, get_user_model()):
                return self.owner_object.get_absolute_url()
        except AttributeError:
            pass
        return "/"

@python_2_unicode_compatible
class Plugget(models.Model):
    """A plugget is a graphical element hosted on a Region.
    """
    region = models.ForeignKey(Region, related_name='pluggets', verbose_name=_('region'))
    title = models.CharField(max_length=100, verbose_name=_('title'))
    description = models.TextField(blank=True, null=True, verbose_name=_('description'))
    source = models.CharField(max_length=256, verbose_name=_('source'))
    template = models.CharField(max_length=256, default="pluggets/base_plugget.html", verbose_name=_('template'))
    context = models.TextField(blank=True, null=True, validators=[validate_json], help_text=_('Use the JSON syntax.'), verbose_name=_('context'))
    sort_order = models.PositiveIntegerField(default=0, verbose_name=_('sort order'))

    class Meta:
        ordering = ('region', 'sort_order', 'title',)
        verbose_name = _('plugget')
        verbose_name_plural = _('pluggets')
        unique_together = ('region', 'title')

    def __str__(self):
        return "%s | %s" % (self.region, self.title)
        
    def slug(self):
        return slugify("%s_%s" % (self.region, self.title))

    def get_absolute_url(self):
        return self.region.get_absolute_url()

    @models.permalink
    def get_edit_url(self):
        return ('plugget_edit', (), {"pk": self.pk})

    @models.permalink
    def get_delete_url(self):
        return ('plugget_delete', (), {"pk": self.pk})
