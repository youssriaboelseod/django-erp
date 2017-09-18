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


from unittest import expectedFailure
from django.test import TestCase

from ..loading import registry

class SourceCacheLoadingTestCase(TestCase):        
    def test_register_source(self):
        """Tests registering of new plugget sources.
        """
        def foo(context):
            return context
            
        title = "plugget"
        registry.register_plugget_source(foo, title)
        sources = registry.get_plugget_sources()
        self.assertTrue(title in sources)
        self.assertEqual(sources[title].get("func", None), foo)
        
    def test_register_simple_source(self):
        """Tests registering a simple plugget source.
        """
        title = "simple plugget"
        registry.register_simple_plugget_source(title)
        sources = registry.get_plugget_sources()
        self.assertTrue(title in sources)
        self.assertEqual(sources[title].get("func", None), registry.default_func)
        
    def test_get_source(self):
        """Tests retrieving a specific plugget source, giving its title.
        """        
        registry.register_simple_plugget_source("Plugget 1")
        
        self.assertEqual(
            registry.get_plugget_source("Plugget 1"),
            {
                "func": registry.default_func,
                "description": "A simple plugget.",
                "default_template": "pluggets/base_plugget.html",
                "form": None
            }
        )
        
    @expectedFailure
    def test_get_source_choices(self):
        """Tests retrieving a list of choices for the registered plugget sources.
        """
        registry.clear()
        registry.discovered = True
        
        registry.register_simple_plugget_source("Plugget 1")
        registry.register_simple_plugget_source("Plugget 2")
        
        self.assertEqual(
            registry.get_plugget_source_choices(),
            [
                ("Plugget 1", "Plugget 1"),
                ("Plugget 2", "Plugget 2"),
            ]
        )
        
        self.assertTrue(
            ("Text plugget", "Text plugget") in registry.get_plugget_source_choices(True)
        )
        
    def test_unique_source_title(self):
        """Tests that plugget source titles must be unique.
        """
        def foo_func1(context): return context
        def foo_func2(context): return context
        
        title = "plugget"
        
        registry.register_plugget_source(foo_func1, title)
        self.assertEqual(registry.get_plugget_sources()[title]["func"], foo_func1)
        registry.register_plugget_source(foo_func2, title)  
        self.assertEqual(registry.get_plugget_sources()[title]["func"], foo_func2)
        
    def test_inspected_title(self):
        """Tests inspection of source title from its docstring.
        """
        def foo_func(context):
            """A foo plugget.
            """
            return context
            
        registry.register_plugget_source(foo_func)
        sources = registry.get_plugget_sources()
        
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
            
        registry.register_plugget_source(foo_func)
        sources = registry.get_plugget_sources()
        
        self.assertEqual(sources["A foo plugget with description"]["description"], "With a foo description. Multiline.")
        
    @expectedFailure
    def test_source_cache_auto_discovering(self):
        """Tests the auto-discovering of plugget sources.
        """
        self.assertTrue("Text plugget" in registry.get_plugget_sources(True))
     
    def test_source_cache_clearing(self):
        """Tests clearing of plugget sources.
        """
        registry.register_simple_plugget_source("Garbage")
        
        self.assertEqual(registry.discovered, True)
        self.assertTrue(len(registry.get_plugget_sources()) > 0)
        
        registry.clear()
        
        self.assertEqual(registry.discovered, False)
        self.assertEqual(len(registry.get_plugget_sources()), 0)
