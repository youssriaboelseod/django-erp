# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models, migrations


def install(apps, schema_editor):
    Group = apps.get_model('core.Group')
    Permission = apps.get_model('core.Permission')

    users_group, is_new = Group.objects.get_or_create(name="users")
    view_notification, is_new = Permission.objects.get_or_create_by_natural_key("view_notification", "notifications", "notification")
    
    # Permissions.
    users_group.permissions.add(view_notification)


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
        ('core', '0002_initial_fixture'),
    ]

    operations = [
        migrations.RunPython(install),
    ]
