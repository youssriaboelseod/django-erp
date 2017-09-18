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


from functools import wraps
from django.shortcuts import redirect
from django.utils.decorators import available_attrs

from .models import Plugget
import collections


def is_plugget_editable(get_plugget_func, redirect_to='/'):
    """Checks if the plugget returned by "get_plugget_func" is editable or not.
    
    A plugget is editable if its source UID is registered.
    """
    def decorator(viewfunc):
        @wraps(viewfunc, assigned=available_attrs(viewfunc))
        def _wrapped_view(request, *args, **kwargs):
            from .loading import registry
            plugget = None
            if isinstance(get_plugget_func, collections.Callable):
                plugget = get_plugget_func(request, *args, **kwargs)
            if plugget\
            and (not isinstance(plugget, Plugget)\
                or (plugget.source not in registry.get_plugget_sources())):
                return redirect(redirect_to)
            return viewfunc(request, *args, **kwargs)
        return _wrapped_view
    return decorator
