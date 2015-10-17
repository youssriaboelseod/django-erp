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


from copy import copy
from django.conf import settings
from django.db import models
from django.utils.encoding import force_text
from django import template
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from djangoerp.core.utils.models import (
    get_model,
    get_fields,
    get_field_type,
    get_field_tuple,
)


register = template.Library()


@register.filter
def typeof(value):
    """Returns the type of the given value.

    Example usage: {{ my_var|typeof }}
    """
    return (u"%s" % type(value)).replace("<class '", "").replace("<type '", "").replace("'>", "")


@register.filter
def model_name(obj):
    """Returns the model name for the given instance.

    Example usage: {{ object|model_name }}
    """
    try:
        mk = get_model(obj)
        return force_text(mk._meta.verbose_name)
    except:
        pass
    return ""


@register.filter
def model_name_plural(obj):
    """Returns the pluralized model name for the given instance.

    Example usage: {{ object|model_name_plural }}
    """
    try:
        mk = get_model(obj)
        return force_text(mk._meta.verbose_name_plural)
    except:
        pass
    return ""


@register.filter
def raw_model_name(obj):
    """Returns the raw model name for the given instance.

    Example usage: {{ object|raw_model_name }}
    """
    try:
        mk = get_model(obj)
        return mk.__name__.lower()
    except:
        pass
    return ""


@register.filter
def raw_model_name_plural(obj):
    """Returns the raw pluralized model name for the given instance.

    Example usage: {{ object|raw_model_name_plural }}
    """
    name = raw_model_name(obj)
    if name:
        return u"%ss" % name
    return ""
    

@register.simple_tag(takes_context=True)
def render_model_list(context, object_list, field_list=[], template_name=None, uid=""):
    """Renders a table with given fields for all given model instances.
    
    It takes three optional arguments:
    
     * field_list -- The list of field names to be rendered [default: all].
     * template_name -- Template that renders the list [default: elements/table_list.html]
     * uid -- An universal ID for this model list (must be unique in the template context).

    Example tag usage: {% render_model_list object_list [fields] [template_name] %}
    """
    if not isinstance(object_list, models.query.QuerySet):
        return ""
        
    if not field_list:
        field_list = []
        
    prefix = ""
    if uid:
        prefix = "%s_" % uid
        
    model = object_list.model
    fields = [model._meta.get_field(n) for n in field_list] or model._meta.fields
    filters = dict([(f.attname, ("", "")) for f in fields])
    filters.update(context.get("%slist_filter_by" % prefix, None) or {})
    headers = [{"name": f.verbose_name, "attname": f.attname, "type": get_field_type(f), "filter": {"expr": filters[f.attname][0], "value": filters[f.attname][1]}} for f in fields]
    rows = [{"object": o, "fields": [f.value_to_string(o) for f in fields]} for o in object_list]
    new_context = copy(context)
    new_context.update(
        {
            "table": {
                "uid": uid,
                "order_by": object_list.query.order_by,
                "headers": headers,
                "rows": rows
            }
        }
    )
    
    return render_to_string(template_name or settings.MODEL_LIST_DEFAULT_TEMPLATE, new_context)


@register.simple_tag(takes_context=True)
def render_model_details(context, objects, field_layout=[], template_name=None, uid=""):
    """Renders a details table from one or more model forms and/or instances.
    
    it could be also possible to specify the layout of the table, using the
    "field_layout" argument which takes a list (of lists) of field names. You
    can use it to specify not only which field goes in which row, but also if
    two or more fields should be rendered on the same row.

    Example tag usage: {% render_model_details "[object, form]" "[field1, [0.field2, 1.field3], field4]" %}
    """
    if objects and isinstance(objects, basestring):
        objects = eval(objects, {}, context)
    if not isinstance(objects, (list, tuple)):
        objects = [objects]
    
    if isinstance(field_layout, basestring) and field_layout:
        field_layout = eval(field_layout)
    elif not field_layout:
        field_layout = []
        
    def make_layout(field_list, objects):
        return_list = []
        for f in field_list:
            if isinstance(f, (tuple, list)):
                return_list.append([l[0] for l in make_layout(f, objects)])
            else:
                on, s, fn = f.rpartition('.')
                if on and fn:
                    o = objects[int(on)]
                elif not on:
                    o = objects[0]
                if o:
                    label, attrs, value = get_field_tuple(fn, o)
                    return_list.append([{"name": label, "attrs": attrs, "value": value}])
        return return_list
        
    layout = make_layout(field_layout, objects)
            
    if not field_layout:
        for o in objects:
            for f in get_fields(o):
                #if isinstance(f, (list, tuple)):
                #    f = f[0]
                label, attrs, value = get_field_tuple(f, o)
                layout.append([{"name": label, "attrs": attrs, "value": value}])
                
    num_cols = 1
    for row in layout:
        num_cols = max(num_cols, len(row))
                
    new_context = copy(context)
    new_context.update(
        {
            "details": {
                "uid": uid,
                "num_cols": num_cols,
                "layout": layout
            }
        }
    )
    
    return render_to_string(template_name or settings.MODEL_DETAILS_DEFAULT_TEMPLATE, new_context)
