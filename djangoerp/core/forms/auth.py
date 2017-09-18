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
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.conf import settings

from . import enrich_form
from ..models import User

class BaseUserCreationForm(UserCreationForm):
    """A base class for all user creation forms.
    """
    class Meta(UserCreationForm.Meta):
        # This is the custom User model, not the Django's one.
        model = get_user_model()

    def clean_password1(self):
        """Checks for a valid password1.
        """
        password1 = self.cleaned_data.get("password1")
            
        if not (password1 or self.instance.pk):
            raise forms.ValidationError(_('This field is required.'))
            
        return password1

    def clean_password2(self):
        """Checks if password2 is equal to password1.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
            
        if (password1 and not password2) or not (password2 or self.instance.pk):
            raise forms.ValidationError(_('This field is required.'))
        
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
            
        return password2
        
class AdminUserCreationForm(BaseUserCreationForm):
    """A form that creates a user with no privileges.
    """
    class Meta(BaseUserCreationForm.Meta):
        fields = '__all__'

class AdminUserChangeForm(UserChangeForm):
    """A form for updating users.
    
    Includes all the fields on the user, but replaces the password field with
    admin's password hash display field.
    """
    class Meta:
        # This is the custom User model, not the Django's one.
        model = User
        fields = '__all__'

class UserForm(BaseUserCreationForm):
    """Form for user data.
    """
    class Meta(BaseUserCreationForm.Meta):
        fields = ['username', 'email', 'password1', 'password2', 'language', 'timezone']
        
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = (self.instance.pk is None)
        self.fields['password2'].required = (self.instance.pk is None)

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        if commit:
            user.save()
            self.save_m2m()
        return user

enrich_form(UserForm)
