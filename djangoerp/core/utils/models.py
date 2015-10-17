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


from django.utils.formats import localize
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.apps import apps as app_registry
from django.db import models
from django import forms
from django.forms.forms import BoundField, pretty_name
from django.forms.utils import flatatt

from .rendering import field_to_string


def get_model(klass):
    """Returns the model class identified by klass.
    
    If klass is already a model class, is returned as it is.
    If klass is a model instance or queryset, its model class is returned.
    If klass is a string, it's used to retrieve the related real model class.
    
    A ValueError is raised on other cases.
    """    
    try:
        if issubclass(klass, models.Model):
            return klass
    except:
        pass
        
    if isinstance(klass, models.Model):
        return klass.__class__
        
    elif isinstance(klass, models.query.QuerySet):
        return klass.model
        
    elif isinstance(klass, basestring):
        app_label, sep, model_name = klass.rpartition('.')
        return app_registry.get_model(app_label, model_name)
        
    raise ValueError
   
     
def get_fields(form_or_model):
    """Returns a dict containing all the fields of the given model/form instance.
    
    If the given instance is not a model mor a form, an empty dict is returned.
    
    The returned dict is in the form:
    
    {field_name: field_instance, ...}
    """
    field_list = {}
    
    if isinstance(form_or_model, models.Model):
        field_list = dict([(f.name, f) for f in (form_or_model._meta.fields + form_or_model._meta.many_to_many)])
    elif isinstance(form_or_model, forms.BaseForm):
        field_list = form_or_model.fields
        
    return field_list


def get_field_type(f):
    """Returns a string representing the type of the given field.
    """
    field_type = f.__class__.__name__.lower().replace("field", "")
    if f.choices:
        field_type += "_choices"
    return field_type

       
def get_field_tuple(name, form_or_model):
    """Returns a tuple for the field, of given instance, identified by "name".
    
    Instance could be a model instance, a form instance or any arbitrary object.
    
    The returned tuple is in the form:
    
    (label, attrs, value)
    """    
    name, sep, suffix = name.partition(':')
    
    label = ""
    value = ""
    td_attrs = {}
    field_list = get_fields(form_or_model)
    field = None
    
    if name in field_list:
        field = field_list[name]
        
    elif hasattr(form_or_model, name):
        field = getattr(form_or_model, name)
        if hasattr(field, 'short_description'):
            name = field.short_description

    if isinstance(field, models.Field):
        label = '%s:' % field.verbose_name
        value = '%s' % field_to_string(field, form_or_model)

    elif isinstance(field, forms.Field):
        bf = BoundField(form_or_model, field, name)
        label = '%s' % bf.label_tag()
        value = '%s' % bf
        if bf.help_text:
            value += '<br/><span title="%(help_text)s" class="helptext helppopup">%(help_text)s</span>' % {"help_text": '%s' % bf.help_text}
        errors = bf.errors
        if errors:
            value += '<br/>\n<ul class="errorlist">\n'
            for error in errors:
                value += '\t<li>%s</li>\n' % error
            value += '</ul>\n'
        css_classes = bf.css_classes()
        if css_classes:
            td_attrs['class'] = css_classes

    else:
        name = _(pretty_name(name).lower())
        label = '%s:' % name.capitalize()
        value = field() if callable(field) else field

    firstcap_label = label[:1].upper() + label[1:]
    if suffix:
        value += " " + suffix

    return mark_safe(firstcap_label), flatatt(td_attrs), mark_safe(value)

