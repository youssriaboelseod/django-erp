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


import collections
from django.utils import six
from djangoerp.core.cache import Singleton


@six.add_metaclass(Singleton)
class PluggetSourceCache(object):
    """Stores all plugget sources.
    """

    def __init__(self):
        self.default_func = lambda x: x
        self.clear()
        self.auto_discover()
        
    def register(self, func, title, description, template, form):        
        if not isinstance(func, collections.Callable):
            func = self.default_func
            
        import inspect
            
        doc = inspect.getdoc(func) or ""
        insp_title, sep, insp_description = doc.partition("\n")
        title = title or insp_title.strip("\n.") or func.__name__.capitalize()
        self.__sources[title] = {
            "func": func,
            "description": description or insp_description.strip("\n").replace("\n\n", " ").replace("\n", " "),
            "default_template": template,
            "form": form
        }
            
    def clear(self):
        self.discovered = False
        self.__sources = {}

    @property
    def sources(self):
        self.auto_discover()
        return self.__sources

    def get_source_choices(self):
        return [(k, k) for k, s in list(self.sources.items())]
    
    def auto_discover(self):
        """ Auto discover pluggets of installed applications.
        """
        from django.conf import settings
     
        if self.discovered:
            return
            
        for app in settings.INSTALLED_APPS:
            # Skip Django's apps.
            if app.startswith('django.'):
                continue
                
            # Try to import pluggets from the current app.
            module_name = "%s.pluggets" % app

            try:
                module = __import__(module_name, {}, {}, ['*'])
            except ImportError:
                pass
                
        self.discovered = True

    def register_plugget_source(self, func, title=None, description=None, template="pluggets/base_plugget.html", form=None):
        """Register a new plugget source.
        
        A plugget source is identified by:
        
         * func -- A callable which takes a context, manupulates and returns it.
         * title -- A default title for the plugget [optional]. If title is already
                    registered, old plugget source will be replaced by new one.
                    (default: title specified in func's docstring or its name)
         * description -- A description of purpose of the plugget [optional].
                          (default: the remaining part of func's docstring)
         * template -- Path of template that must be used to render the plugget.
         * form -- The form to be used for plugget customization.
        
        Please note that title must be unique because it's used as key in the
        register dictionary and is the univoque identifier of a specific source.
        """
        self.register(func, title, description, template, form)

    def register_simple_plugget_source(self, title, description="A simple plugget.", template="pluggets/base_plugget.html", form=None):
        """Register a new simplified plugget source.
        
        This is a convenient function to simplify registration of plugget sources
        that do not change the current context (a dummy function is used).
        
         * title -- A default title for the plugget. If title is already registered,
                    old plugget source will be replaced by new one.
         * description -- A description of purpose of the plugget [optional].
                          (default: default description string)
         * template -- Path of template that must be used to render the plugget.
         * form -- The form to be used for plugget customization.
        
        Please note that title must be unique because it's used as key in the
        register dictionary and is the univoque identifier of a specific source.
        """
        self.register(None, title, description, template, form)
        
    def get_plugget_sources(self, force_discovering=False):
        """Returns the list of all registered plugget sources.
        
        If force_discovering is True, a complete auto discovering of plugget sources
        is forced.
        """
        if force_discovering:
            self.discovered = False
        return self.sources
        
    def get_plugget_source(self, source_title, force_discovering=False):
        """Returns the registered plugget sources identified by "source_title".
        
        If the source is not registered, None is returned.
        
        If force_discovering is True, a complete auto discovering of plugget sources
        is forced.
        """
        return self.get_plugget_sources(force_discovering).get(source_title, None)
        
    def get_plugget_source_choices(self, force_discovering=False):
        """Returns all registered plugget sources as a choice list for forms.
        
        A choice is a tuple in the form (source_title, source_uid).
        
        If force_discovering is True, a complete auto discovering of plugget sources
        is forced.
        """
        if force_discovering:
            self.discovered = False
        return self.get_source_choices()


registry = PluggetSourceCache()
