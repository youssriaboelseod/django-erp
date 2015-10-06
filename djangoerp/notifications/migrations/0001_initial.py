# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models, migrations
import djangoerp.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('signature', models.CharField(max_length=50, verbose_name='signature')),
                ('template', models.CharField(default=None, max_length=200, null=True, verbose_name='template', blank=True)),
                ('context', models.TextField(blank=True, help_text='Use the JSON syntax.', null=True, verbose_name='context', validators=[djangoerp.core.models.validate_json])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('backlink', models.CharField(max_length=200, null=True, verbose_name='backlink', blank=True)),
                ('source_id', models.PositiveIntegerField()),
                ('source_content_type', models.ForeignKey(related_name='+', to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name': 'activity',
                'verbose_name_plural': 'activities',
            },
        ),
        migrations.CreateModel(
            name='FollowRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('followed_id', models.PositiveIntegerField()),
                ('follower_id', models.PositiveIntegerField()),
                ('followed_content_type', models.ForeignKey(related_name='+', to='contenttypes.ContentType')),
                ('follower_content_type', models.ForeignKey(related_name='+', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'follow relation',
                'verbose_name_plural': 'follow relations',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('target_id', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('read', models.DateTimeField(null=True, verbose_name='read on', blank=True)),
                ('dispatch_uid', models.CharField(max_length=32, verbose_name='dispatch UID')),
            ],
            options={
                'get_latest_by': '-created',
                'ordering': ('-created', 'id'),
                'verbose_name_plural': 'notifications',
                'verbose_name': 'notification',
            },
        ),
        migrations.CreateModel(
            name='Signature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'signature',
                'verbose_name_plural': 'signatures',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subscriber_id', models.PositiveIntegerField()),
                ('send_email', models.BooleanField(default=True, verbose_name='send email')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='email', blank=True)),
                ('signature', models.ForeignKey(to='notifications.Signature')),
                ('subscriber_content_type', models.ForeignKey(related_name='+', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'subscription',
                'verbose_name_plural': 'subscriptions',
            },
        ),
        migrations.AddField(
            model_name='notification',
            name='signature',
            field=models.ForeignKey(verbose_name='signature', to='notifications.Signature'),
        ),
        migrations.AddField(
            model_name='notification',
            name='target_content_type',
            field=models.ForeignKey(related_name='+', to='contenttypes.ContentType'),
        ),
        migrations.AlterUniqueTogether(
            name='notification',
            unique_together=set([('target_content_type', 'target_id', 'dispatch_uid')]),
        ),
        migrations.AlterIndexTogether(
            name='notification',
            index_together=set([('target_content_type', 'target_id', 'dispatch_uid')]),
        ),
    ]
