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

from hashlib import md5
from django import template

register = template.Library()

@register.simple_tag
def avatar(email, size=32, default="mm", css_class="avatar image"):
    """Returns the gravatar image associated to the given email.
    
    More info: http://www.gravatar.com

    Example tag usage: {% avatar email_address 80 "http://.../my_default_image.jpg" [css_class] %}
    """        
    # Creates and returns the URL.
    h = ""
    if email:
        h = md5(email.encode('utf-8')).hexdigest()
    url = 'http://www.gravatar.com/avatar/%s?s=%s&r=g' % (h, size)
    
    # Adds a default image URL (if present).
    if default:
        url = "%s&d=%s" % (url, default)
        
    return '<img class="%s" width="%s" height="%s" src="%s" />' % (css_class, size, size, url)

