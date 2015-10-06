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

import hashlib, json
from datetime import datetime
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from djangoerp.core.models import validate_json
from djangoerp.core.utils.rendering import field_to_string

from .managers import *


@python_2_unicode_compatible
class FollowRelation(models.Model):
    """It represents a relation  model between a watcher and a watched object.
    """
    followed_content_type = models.ForeignKey(ContentType, related_name="+")
    followed_id = models.PositiveIntegerField()
    followed = GenericForeignKey('followed_content_type', 'followed_id')
    follower_content_type = models.ForeignKey(ContentType, related_name="+")
    follower_id = models.PositiveIntegerField()
    follower = GenericForeignKey('follower_content_type', 'follower_id')

    objects = FollowRelationManager()
    
    class Meta:
        verbose_name = _('follow relation')
        verbose_name_plural = _('follow relations')

    def __str__(self):
        return _("%s followed by %s") % (self.followed, self.follower)

@python_2_unicode_compatible
class Signature(models.Model):
    """It represents the identifier of an activity and/or a notification.
    """
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)

    class Meta:
        verbose_name = _('signature')
        verbose_name_plural = _('signatures')

    def __str__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        if self.slug and not self.title:
            from django.forms.forms import BoundField, pretty_name
            self.title = pretty_name(self.slug).replace("-", " ").capitalize()
        super(Signature, self).save(*args, **kwargs)
 
@python_2_unicode_compatible       
class Subscription(models.Model):
    """A Subscription allows a per-signature-based filtering of notifications.
    """
    subscriber_content_type = models.ForeignKey(ContentType, related_name="+")
    subscriber_id = models.PositiveIntegerField()
    subscriber = GenericForeignKey('subscriber_content_type', 'subscriber_id')
    signature = models.ForeignKey(Signature)
    send_email = models.BooleanField(default=True, verbose_name=_('send email'))
    email = models.EmailField(null=True, blank=True, verbose_name=_('email'))

    objects = SubscriptionManager()

    class Meta:
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')

    def __str__(self):
        return "%s | %s" % (self.subscriber, self.signature)

@python_2_unicode_compatible
class Activity(models.Model):
    """An activity is a registered event that happens at a specific time.
    
    It can be notified by many notifications to many watcher objects.
    """
    title = models.CharField(_('title'), max_length=200)
    signature = models.CharField(_('signature'), max_length=50)
    template = models.CharField(_('template'), blank=True, null=True, max_length=200, default=None)
    context = models.TextField(_('context'), blank=True, null=True, validators=[validate_json], help_text=_('Use the JSON syntax.'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    backlink = models.CharField(_('backlink'), blank=True, null=True, max_length=200)
    source_content_type = models.ForeignKey(ContentType, related_name="+")
    source_id = models.PositiveIntegerField()
    source = GenericForeignKey('source_content_type', 'source_id')

    objects = ActivityManager()
    
    class Meta:
        verbose_name = _('activity')
        verbose_name_plural = _('activities')
        ordering = ('-created',)

    def __str__(self):
        try:
            return self.title % self.get_context()
        except KeyError:
            return self.title

    def get_context(self):
        return json.loads(str(self.context or "{}"))
        
    def get_template_name(self):
        return self.template or "notifications/activities/%s.html" % self.signature

    def get_content(self):
        from django.template import TemplateDoesNotExist
        try:
            return render_to_string(self.get_template_name(), self.get_context())
        except: # Catching all exceptions avoid any rendering issue.
            return ""
        
    def get_absolute_url(self):
        return self.backlink or ""

python_2_unicode_compatible
class Notification(models.Model):
    """A notification notifies a specific event to a specific target.
    """
    title = models.CharField(max_length=100, verbose_name=_('title'))
    description = models.TextField(blank=True, null=True, verbose_name=_('description'))
    target_content_type = models.ForeignKey(ContentType, related_name="+")
    target_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_content_type', 'target_id')
    signature = models.ForeignKey(Signature, verbose_name=_('signature'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created on'))
    read = models.DateTimeField(blank=True, null=True, verbose_name=_('read on'))
    dispatch_uid = models.CharField(max_length=32, verbose_name=_('dispatch UID'))

    objects = NotificationManager()

    class Meta:
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')
        ordering = ('-created', 'id')
        get_latest_by = '-created'
        unique_together = (
            ("target_content_type", "target_id", "dispatch_uid"),
        )
        index_together = (
            ("target_content_type", "target_id", "dispatch_uid"),
        )

    def __str__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('notification_detail', (), {"object_model": self.target._meta.verbose_name_plural, "object_id": self.target.pk, "pk": self.pk})

    @models.permalink
    def get_delete_url(self):
        return ('notification_delete', (), {"object_model": self.target._meta.verbose_name_plural, "object_id": self.target.pk, "pk": self.pk})

    def clean_fields(self, exclude=None):
        if not self.dispatch_uid:
            token = "%s%s%s" % (self.title, self.description, datetime.now())
            self.dispatch_uid = hashlib.md5(token.encode('utf-8')).hexdigest()
        """if not Subscription.objects.filter(subscriber=self.target, signature=self.signature):
            raise ValidationError('The target is not subscribed for this kind of notification.')"""
        super(Notification, self).clean_fields(exclude)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Notification, self).save(*args, **kwargs)

class Observable(object):
    """Mix-in that sends a special signal when a field is changed.
    
    It also offers a simple API to manage followers.
    """
    __change_exclude = []
    __subscriber_fields = []
    
    def __init__(self, *args, **kwargs):
        super(Observable, self).__init__(*args, **kwargs)
        self.__changes = {}
        self.__field_cache = dict([(f.attname, f) for f in (self._meta.fields)])
        self.__followers_cache = None

    def __setattr__(self, name, value):
        try:
            if self.pk and name in self.__field_cache:
                field = self.__field_cache[name]
                label = "%s" % field.verbose_name
                if name not in self.__change_exclude:
                    old_value = field_to_string(field, self)
                    if label in self.__changes:
                        old_value = self.__changes[label][0]
                    super(Observable, self).__setattr__(name, value)
                    value = field_to_string(field, self)
                    if value != old_value:
                        self.__changes[label] = ("%s" % old_value, "%s" % value)
                return

        except:
            pass
        
        super(Observable, self).__setattr__(name, value)

    def followers(self):
        """Returns the list of the current followers.
        """
        if self.__followers_cache:
            return self.__followers_cache
        return [r.follower for r in FollowRelation.objects.filter(followed=self)]
        
    def is_followed_by(self, followers):  
        """Checks if all given instances are followers of this object.
        """      
        if not isinstance(followers, (tuple, list)):
            followers = [followers]
            
        cache_followers = self.followers()
        
        for follower in followers:
            found = False
            for cache_follower in cache_followers:
                if follower == cache_follower:
                    found = True
            if not found:
                return False
                
        return True

    def add_followers(self, followers):
        """Registers the given followers.
        """
        if not isinstance(followers, (tuple, list)):
            followers = [followers]

        for f in followers:
            if isinstance(f, models.Model):
                FollowRelation.objects.get_or_create(follower=f, followed=self)

    def remove_followers(self, followers):
        """Unregisters the given followers.
        """
        if not isinstance(followers, (tuple, list)):
            followers = [followers]

        for f in followers:
            if isinstance(f, models.Model):
                FollowRelation.objects.filter(follower=f, followed=self).delete()

class NotificationTarget(object):
    """Mix-in that adds some useful methods to retrieve related notifications.
    """
    def _notification_set(self):
        return Notification.objects.for_object(self)
    notification_set = property(_notification_set)
