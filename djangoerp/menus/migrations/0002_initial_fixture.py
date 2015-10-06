# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models, migrations
from django.utils.translation import ugettext_noop as _
from django.core.urlresolvers import reverse

from ..utils import create_detail_actions, create_detail_navigation


def install(apps, schema_editor):
    # Models.
    User = apps.get_model('core.User')
    Group = apps.get_model('core.Group')
    Permission = apps.get_model('core.Permission')
    Menu = apps.get_model('menus.Menu')
    Link = apps.get_model('menus.Link')

    # Instances.
    users_group, is_new = Group.objects.get_or_create(name="users")
    add_bookmark, is_new = Permission.objects.get_or_create_by_natural_key("add_link", "menus", "Link")
    edit_user, is_new = Permission.objects.get_or_create_by_natural_key("change_user", "core", "User")
    delete_user, is_new = Permission.objects.get_or_create_by_natural_key("delete_user", "core", "User")
    
    # Menus.
    main_menu, is_new = Menu.objects.get_or_create(
        slug="main",
        description=_("Main menu")
    )
    
    user_area_not_logged_menu, is_new = Menu.objects.get_or_create(
        slug="user_area_not_logged",
        description=_("User area for anonymous users")
    )
    
    user_area_logged_menu, is_new = Menu.objects.get_or_create(
        slug="user_area_logged",
        description=_("User area for logged users")
    )
    
    user_detail_actions, is_new = create_detail_actions(User)
    user_detail_navigation, is_new = create_detail_navigation(User)
    
    # Links.
    my_dashboard_link, is_new = Link.objects.get_or_create(
        menu_id=main_menu.pk,
        title=_("My Dashboard"),
        slug="my-dashboard",
        description=_("Go back to your dashboard"),
        url="/"
    )
    
    login_link, is_new = Link.objects.get_or_create(
        title=_("Login"),
        slug="login",
        description=_("Login"),
        url=reverse("user_login"),
        only_authenticated=False,
        menu_id=user_area_not_logged_menu.pk
    )
    
    administration_link, is_new = Link.objects.get_or_create(
        title=_("Administration"),
        slug="administration",
        description=_("Administration panel"),
        url="/admin/",
        only_staff=True,
        menu_id=user_area_logged_menu.pk
    )
    
    logout_link, is_new = Link.objects.get_or_create(
        title=_("Logout"),
        slug="logout",
        description=_("Logout"),
        url=reverse("user_logout"),
        menu_id=user_area_logged_menu.pk
    )
    
    user_edit_link, is_new = Link.objects.get_or_create(
        title=_("Edit"),
        slug="user-edit",
        description=_("Edit"),
        url="user_edit",
        context='{"pk": "object.pk"}',
        menu_id=user_detail_actions.pk
    )
    user_edit_link.only_with_perms=[edit_user]
    
    user_delete_link, is_new = Link.objects.get_or_create(
        title=_("Delete"),
        slug="user-delete",
        description=_("Delete"),
        url="user_delete",
        context='{"pk": "object.pk"}',
        menu_id=user_detail_actions.pk
    )
    user_delete_link.only_with_perms=[delete_user]
    
    # Permissions.
    users_group.permissions.add(add_bookmark)


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('core', '0002_initial_fixture'),
    ]

    operations = [
        migrations.RunPython(install),
    ]
