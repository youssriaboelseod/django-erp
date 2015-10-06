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

from django import forms
from django.utils.translation import ugettext_lazy as _
from djangoerp.core.forms import enrich_form

from .models import Menu, Bookmark

class BookmarkForm(forms.ModelForm):
    """Form for bookmark data.
    """
    class Meta:
        model = Bookmark
        fields = ['title', 'url', 'description', 'new_window']
    
    def __init__(self, *args, **kwargs):
        self.menu = kwargs.pop("menu", None)
        super(BookmarkForm, self).__init__(*args, **kwargs)
        if not self.menu:
            try:
                if self.instance and self.instance.menu:
                    self.menu = self.instance.menu
            except Menu.DoesNotExist:
                pass
    
    def clean_title(self):
        title = self.cleaned_data['title']
       
        try:
            bookmark = Bookmark.objects.get(title=title, menu=self.menu)
            if bookmark != self.instance:
                raise forms.ValidationError(_("This title is already in use."))
                
        except Bookmark.DoesNotExist:
            pass
            
        return title
        
    def save(self, commit=True):
        from django.template.defaultfilters import slugify
        
        obj = super(BookmarkForm, self).save(commit=False)
        obj.menu = self.menu or obj.menu
        obj.slug = slugify(("%s_%s" % (obj.title, self.menu.slug))[:-1])
        
        if commit:
            obj.save()
            
        return obj

enrich_form(BookmarkForm)
