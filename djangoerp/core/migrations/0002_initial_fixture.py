# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models, migrations
from django.utils.translation import ugettext_noop as _


def install(apps, schema_editor):
    Group = apps.get_model('core.Group')

    # Groups.
    users_group, is_new = Group.objects.get_or_create(
        name=_('users')
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(install),
    ]
