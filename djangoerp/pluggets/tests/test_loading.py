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
__copyright__ = 'Copyright (c) 2013-2014, django ERP Team'
__version__ = '0.0.5'

from django.test import TestCase

from ..loading import *

class SourceCacheLoadingTestCase(TestCase):        
    def test_register_source(self):
        """Tests registering of new plugget sources.
        """
        def foo(context):
            return context
            
        title = "plugget"
        register_plugget_source(foo, title)
        sources = get_plugget_sources()
        self.assertTrue(title in sources)
        self.assertEqual(sources[title].get("func", None), foo)
        
    def test_register_simple_source(self):
        """Tests registering a simple plugget source.
        """
        title = "simple plugget"
        register_simple_plugget_source(title)
        sources = get_plugget_sources()
        self.assertTrue(title in sources)
        self.assertEqual(sources[title].get("func", None), plugget_source_registry.default_func)
        
    def test_get_source(self):
        """Tests retrieving a specific plugget source, giving its title.
        """        
        register_simple_plugget_source("Plugget 1")
        
        self.assertEqual(
            get_plugget_source("Plugget 1"),
            {
                "func": plugget_source_registry.default_func,
                "description": "A simple plugget.",
                "default_template": "pluggets/base_plugget.html",
                "form": None
            }
        )
        
    def test_get_source_choices(self):
        """Tests retrieving a list of choices for the registered plugget sources.
        """
        plugget_source_registry.clear()
        plugget_source_registry.discovered = True
        
        register_simple_plugget_source("Plugget 1")
        register_simple_plugget_source("Plugget 2")
        
        self.assertEqual(
            get_plugget_source_choices(),
            [
                ("Plugget 1", "Plugget 1"),
                ("Plugget 2", "Plugget 2"),
            ]
        )
        
        self.assertTrue(
            ("Text plugget", "Text plugget") in get_plugget_source_choices(True)
        )
        
    def test_unique_source_title(self):
        """Tests that plugget source titles must be unique.
        """
        def foo_func1(context): return context
        def foo_func2(context): return context
        
        title = "plugget"
        
        register_plugget_source(foo_func1, title)
        self.assertEqual(get_plugget_sources()[title]["func"], foo_func1)
        register_plugget_source(foo_func2, title)  
        self.assertEqual(get_plugget_sources()[title]["func"], foo_func2)
        
    def test_inspected_title(self):
        """Tests inspection of source title from its docstring.
        """
        def foo_func(context):
            """A foo plugget.
            """
            return context
            
        register_plugget_source(foo_func)
        sources = get_plugget_sources()
        
        self.assertTrue("A foo plugget" in sources)
        self.assertEqual(sources["A foo plugget"]["func"], foo_func)
        
    def test_inspected_description(self):
        """Tests inspection of source description from its docstring.
        """
        def foo_func(context):
            """A foo plugget with description.
            
            With a foo description.
            
            Multiline.
            """
            return context
            
        register_plugget_source(foo_func)
        sources = get_plugget_sources()
        
        self.assertEqual(sources["A foo plugget with description"]["description"], "With a foo description. Multiline.")
        
    def test_source_cache_auto_discovering(self):
        """Tests the auto-discovering of plugget sources.
        """
        self.assertTrue("Text plugget" in get_plugget_sources(True))
        
    def test_source_cache_clearing(self):
        """Tests clearing of plugget sources.
        """
        register_simple_plugget_source("Garbage")
        
        self.assertEqual(plugget_source_registry.discovered, True)
        self.assertTrue(len(get_plugget_sources()) > 0)
        
        plugget_source_registry.clear()
        
        self.assertEqual(plugget_source_registry.discovered, False)
        self.assertEqual(len(get_plugget_sources()), 0)
