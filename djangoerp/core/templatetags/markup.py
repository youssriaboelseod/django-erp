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


from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.assignment_tag
def join(join_str, *args):
    """Joins given args (if valid) using join_str.
    
    The result is stored in a context variable.

    Example usage: {% join '/' str1 str2 str3 ... as var %}
    """
    return join_str.join(["%s" % a for a in args if a])


@register.filter
@stringfilter
def split(string, sep):
    """Returns the string split by sep.

    Example usage: {{ request.path|split:"/" }}
    """
    return string.split(sep)


@register.filter
def get(obj, attr_name):
    """Returns the attr value for the given object.

    Example usage: {{ object|get:"pk" }} or {{ object|get:attr_name }}
    """
    if isinstance(obj, dict):
        return obj.get(attr_name, "")

    elif isinstance(obj, (list, tuple))\
    and (isinstance(attr_name, int)\
         or attr_name.isdigit()):
        return obj[attr_name]

    elif hasattr(obj, attr_name):
        value = getattr(obj, attr_name)
        if callable(value):
            return value()
        return value

    return ""
    

@register.filter
def diff(obj, amount):
    """Returns the difference between obj and amount (obj - amount).

    Example usage: {{ my_counter|diff:"5" }} or {{ my_counter|diff:step_id }}
    """
    return obj-float(amount)


@register.filter
@stringfilter
def add_class(value, css_class):
    """Adds a CSS class to an arbitrary HTML tag.

    Please note this filter doesn't check if the class is already assigned.

    Example usage:
        
        {{ my_html_repr|add_class:"col-md-4" }}
        {{ my_html_repr|add_class:my_class }}
    """
    string = unicode(value)
    css_class = unicode(css_class)

    if css_class and string:
        # Look for the very first tag.
        before, sep, after = string.partition('>')
        if before[-1] == '/':
            before = before[:-1]
            sep = '/' + sep
            before = before.rstrip()
        new_string = before + ' class="%s"' % css_class + sep + after

        # Try to find an existing class attribute.
        new_before, new_sep, new_after = before.partition('class="')
        if new_after:
            new_string = new_before + new_sep + css_class + " " + new_after + sep + after

        return mark_safe(new_string)

    return string    
