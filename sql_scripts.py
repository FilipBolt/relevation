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


def create_all_users_and_permissions():
    zeljka = create_if_doesnt_exist('zeljka', 'zeljka@gmail.com', 'motika')
    almir = create_if_doesnt_exist('almir', 'almir@gmail.com', 'elezovic')

    mladen = create_if_doesnt_exist('mladen', 'mladen@gmail.com', 'karan')
    jan = create_if_doesnt_exist('jan', 'jan@gmail.com', 'snajder')
    matej = create_if_doesnt_exist('matej', 'matej@gmail.com', 'gjurkovic')
    bojana = create_if_doesnt_exist('bojana', 'bojana@gmail.com', 'dalbelo')

    annotators = create_group_if_doesnt_exist('annotators')
    uploaders = create_group_if_doesnt_exist('uploaders')

    mladen.groups.add(uploaders)
    jan.groups.add(uploaders)
    matej.groups.add(uploaders)
    bojana.groups.add(uploaders)

    zeljka.groups.add(annotators)
    almir.groups.add(annotators)

    upload_qrels = ContentType.objects.get(app_label='judgementapp', model='query')
    upload_docs = ContentType.objects.get(app_label='judgementapp', model='document')
    judge = ContentType.objects.get(app_label='judgementapp', model='judgement')

    can_upload_qrels = create_permission_if_doesnt_exist('can_upload_queries', "Can Upload Query", upload_qrels)
    can_upload_docs = create_permission_if_doesnt_exist('can_upload_docs', "Can Upload Document", upload_docs)
    can_judge = create_permission_if_doesnt_exist('can_judge', "Can Judge", judge)

    uploaders.permissions.add(can_upload_qrels)
    uploaders.permissions.add(can_upload_docs)
    uploaders.permissions.add(can_judge)

    annotators.permissions.add(can_judge)
    annotators.permissions.add(can_upload_qrels)


# hints if doesn't work or simply use python manage.py shell
# export DJANGO_SETTINGS_MODULE=relevation.settings
# import django; django.setup()
