# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models, migrations
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_noop as _


def install(apps, schema_editor):
    Menu = apps.get_model('menus.Menu')
    Link = apps.get_model('menus.Link')

    user_area_not_logged_menu, is_new = Menu.objects.get_or_create(slug="user_area_not_logged")
    
    # Links.
    register_link, is_new = Link.objects.get_or_create(
        title=_("Register"),
        slug="register",
        description=_("Register a new account"),
        url=reverse("user_register"),
        only_authenticated=False,
        menu_id=user_area_not_logged_menu.pk
    )


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
        ('menus', '0002_initial_fixture'),
    ]

    operations = [
        migrations.RunPython(install),
    ]
