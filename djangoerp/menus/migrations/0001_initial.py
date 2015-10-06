# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models, migrations
import djangoerp.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
                ('url', models.CharField(max_length=255, verbose_name='url')),
                ('icon', models.CharField(max_length=100, verbose_name='icon', blank=True)),
                ('template_name', models.CharField(max_length=255, verbose_name='template name', blank=True)),
                ('context', models.TextField(blank=True, help_text='Use the JSON syntax.', null=True, verbose_name='context', validators=[djangoerp.core.models.validate_json])),
                ('description', models.CharField(max_length=255, null=True, verbose_name='description', blank=True)),
                ('new_window', models.BooleanField(default=False, verbose_name='New window')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='sort order')),
                ('only_authenticated', models.BooleanField(default=True, verbose_name='Only for authenticated users')),
                ('only_staff', models.BooleanField(default=False, verbose_name='Only for staff users')),
            ],
            options={
                'ordering': ('menu', 'sort_order', 'id'),
                'verbose_name': 'link',
                'verbose_name_plural': 'links',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='slug')),
                ('description', models.CharField(max_length=200, null=True, verbose_name='description', blank=True)),
                ('template_name', models.CharField(max_length=255, verbose_name='template name', blank=True)),
            ],
            options={
                'verbose_name': 'menu',
                'verbose_name_plural': 'menus',
            },
        ),
        migrations.AddField(
            model_name='link',
            name='menu',
            field=models.ForeignKey(related_name='links', verbose_name='menu', to='menus.Menu'),
        ),
        migrations.AddField(
            model_name='link',
            name='only_with_perms',
            field=models.ManyToManyField(to='auth.Permission', verbose_name='Only with following permissions', blank=True),
        ),
        migrations.AddField(
            model_name='link',
            name='submenu',
            field=models.ForeignKey(related_name='parent_links', db_column='submenu_id', blank=True, to='menus.Menu', null=True, verbose_name='sub-menu'),
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
            ],
            options={
                'verbose_name': 'bookmark',
                'proxy': True,
                'verbose_name_plural': 'bookmarks',
            },
            bases=('menus.link',),
        ),
    ]
