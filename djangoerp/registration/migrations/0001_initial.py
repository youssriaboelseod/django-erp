# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivationToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activation_key', models.CharField(max_length=40, null=True, verbose_name='activation key', blank=True)),
                ('key_expiration', models.DateTimeField(null=True, verbose_name='key expiration', blank=True)),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'activation token',
                'verbose_name_plural': 'activation tokens',
            },
        ),
    ]
