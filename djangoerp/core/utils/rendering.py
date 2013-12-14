#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
__copyright__ = 'Copyright (c) 2013 Emanuele Bertoldi'
__version__ = '0.0.3'

from django.utils.formats import localize
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.db import models
from django import forms
from django.forms.forms import BoundField, pretty_name
from django.forms.util import flatatt

def value_to_string(value):
    """Tries to return a smart string representation of the given value.
    """
    output = localize(value)

    if isinstance(value, (list, tuple)):
        output = ', '.join([value_to_string(v) for v in value])

    elif isinstance(value, bool):
        if value:
            output = render_to_string('elements/yes.html', {})
        else:
            output = render_to_string('elements/no.html', {})

    elif isinstance(value, float):
        output = u'%.2f' % value

    elif isinstance(value, int):
        output = '%d' % value

    if not value and not output:
        output = render_to_string('elements/empty.html', {})

    return mark_safe(output.strip())

def field_to_value(field, instance):
    """Tries to convert a model field value in something smarter to render.
    """
    value = getattr(instance, field.name)

    if field.primary_key or isinstance(field, (models.SlugField, models.PositiveIntegerField)):
        if value:
          return u'#%s' % value

    elif isinstance(field, (models.ForeignKey, models.OneToOneField)):
        try:
            return render_to_string('elements/link.html', {'url': value.get_absolute_url(), 'caption': value})
        except AttributeError:
            return value

    elif isinstance(field, models.ManyToManyField):
        items = []
        for item in value.all():
            try:
                items.append(render_to_string('elements/link.html', {'url': item.get_absolute_url(), 'caption': item}))
            except AttributeError:
                items.append(u'%s' % item)
        return items

    elif isinstance(field, models.URLField) and value:
        return render_to_string('elements/link.html', {'url': value, 'caption': value})

    elif isinstance(field, models.EmailField) and value:
        return render_to_string('elements/link.html', {'url': 'mailto:%s' % value, 'caption': value})

    elif field.choices:
        return getattr(instance, 'get_%s_display' % field.name)()

    elif isinstance(field, models.BooleanField):
        if value == '0' or not value:
            return False
        return True

    return value

def field_to_string(field, instance):
    """All-in-one conversion from a model field value to a smart string representation.
    """
    return value_to_string(field_to_value(field, instance))

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
    from . import get_fields
    
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
        label = u'%s:' % field.verbose_name
        value = field_to_string(field, form_or_model)

    elif isinstance(field, forms.Field):
        bf = BoundField(form_or_model, field, name)
        label = u'%s' % bf.label_tag()
        value = u'%s' % bf
        if bf.help_text:
            value += '<br/><span title="%(help_text)s" class="helptext helppopup">%(help_text)s</span>' % {"help_text": u'%s' % bf.help_text}
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
        label = u'%s:' % name.capitalize()
        if callable(field):
            value = value_to_string(field())
        else:
            value = value_to_string(field)

    return mark_safe(label[:1].capitalize() + label[1:]), flatatt(td_attrs), mark_safe(" ".join([t for t in (value, suffix) if t]))
