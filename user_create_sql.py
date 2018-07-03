from django.contrib.auth.models import User, Group, Permission
from django.db import IntegrityError
from django.contrib.contenttypes.models import ContentType


def create_if_doesnt_exist(name, email, password):
    try:
        user = User.objects.create_user(name, email, password)
        user.save()
    except IntegrityError:
        print('user {} exists'.format(name))
        user = User.objects.get(username=name)
    else:
        print('create user {}'.format(name))

    return user


def create_group_if_doesnt_exist(name):
    try:
        group = Group.objects.create(name=name)
        group.save()
    except IntegrityError:
        print('group {} exists'.format(name))
        group = Group.objects.get(name=name)
    else:
        print('created group {}'.format(name))

    return group


def create_permission_if_doesnt_exist(codename, desc, content_type):
    try:
        permission = Permission(
            name=desc, codename=codename, content_type=content_type
        )
        permission.save()
    except IntegrityError:
        print('permission {} exists'.format(codename))
        permission = Permission.objects.get(codename=codename)
    else:
        print('created permission {}'.format(codename))

    return permission
