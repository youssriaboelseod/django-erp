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
            name='Plugget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('source', models.CharField(max_length=256, verbose_name='source')),
                ('template', models.CharField(default='pluggets/base_plugget.html', max_length=256, verbose_name='template')),
                ('context', models.TextField(blank=True, help_text='Use the JSON syntax.', null=True, verbose_name='context', validators=[djangoerp.core.models.validate_json])),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='sort order')),
            ],
            options={
                'ordering': ('region', 'sort_order', 'title'),
                'verbose_name': 'plugget',
                'verbose_name_plural': 'pluggets',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='slug')),
                ('title', models.CharField(max_length=256, null=True, verbose_name='title', blank=True)),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'verbose_name': 'region',
                'verbose_name_plural': 'regions',
            },
        ),
        migrations.AddField(
            model_name='plugget',
            name='region',
            field=models.ForeignKey(related_name='pluggets', verbose_name='region', to='pluggets.Region'),
        ),
        migrations.AlterUniqueTogether(
            name='plugget',
            unique_together=set([('region', 'title')]),
        ),
    ]
