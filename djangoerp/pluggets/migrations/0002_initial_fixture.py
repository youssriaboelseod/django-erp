# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models, migrations
from django.utils.translation import ugettext_noop as _


def install(apps, schema_editor):
    Group = apps.get_model('core.Group')
    Permission = apps.get_model('core.Permission')
    Region = apps.get_model('pluggets.Region')
    Plugget = apps.get_model('pluggets.Plugget')

    users_group, is_new = Group.objects.get_or_create(name="users")
    add_plugget, is_new = Permission.objects.get_or_create_by_natural_key("add_plugget", "pluggets", "plugget")
    
    # Regions.
    footer_region, is_new = Region.objects.get_or_create(
        slug="footer",
        title=_("Footer")
    )
    
    sidebar_region, is_new = Region.objects.get_or_create(
        slug="sidebar",
        title=_("Sidebar")
    )
    
    # Pluggets.
    main_menu_plugget, is_new = Plugget.objects.get_or_create(
        title=_("Main menu"),
        source="djangoerp.pluggets.pluggets.menu",
        template="pluggets/menu.html",
        context='{"name": "main"}',
        region_id=sidebar_region.pk
    )
    
    powered_by_plugget, is_new = Plugget.objects.get_or_create(
        title=_("Powered by"),
        description=_('Shows a classic "Powered by XYZ" claim.'),
        source="djangoerp.pluggets.pluggets.text",
        template="pluggets/powered-by.html",
        context='{"name": "django ERP", "url": "https://github.com/djangoERPTeam/django-erp"}',
        region_id=footer_region.pk
    )
    
    # Permissions.
    users_group.permissions.add(add_plugget)


class Migration(migrations.Migration):

    dependencies = [
        ('pluggets', '0001_initial'),
        ('core', '0002_initial_fixture'),
    ]

    operations = [
        migrations.RunPython(install),
    ]
