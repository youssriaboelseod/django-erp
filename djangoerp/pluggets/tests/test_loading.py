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
__version__ = '0.0.4'

from django.test import TestCase

from ..loading import register_plugget, get_plugget_sources

class SourceCacheLoadingTestCase(TestCase):     
    def test_register_source(self):
        """Tests registering of new plugget sources.
        """
        def foo(context): return context
        title = "plugget"
        register_plugget(foo, title)
        sources = get_plugget_sources()
        self.assertTrue(title in sources)
        self.assertEqual(sources[title].get("func", None), foo)
        
    def test_unique_source_title(self):
        """Tests that plugget source titles must be unique.
        """
        def foo_func1(context): return context
        def foo_func2(context): return context
        
        title = "plugget"
        
        register_plugget(foo_func1, title)
        self.assertEqual(get_plugget_sources()[title]["func"], foo_func1)
        register_plugget(foo_func2, title)  
        self.assertEqual(get_plugget_sources()[title]["func"], foo_func2)
        
    def test_inspected_title(self):
        """Tests inspection of source title from its docstring.
        """
        def foo_func(context):
            """A foo plugget.
            """
            return context
            
        register_plugget(foo_func)
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
            
        register_plugget(foo_func)
        sources = get_plugget_sources()
        
        self.assertEqual(sources["A foo plugget with description"]["description"], "With a foo description. Multiline.")
        
    def test_source_cache_auto_discovering(self):
        """Tests the auto-discovering of plugget sources.
        """
        self.assertTrue("Text plugget" in get_plugget_sources())
