# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judgementapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='query',
            unique_together=set([('qId', 'annotator')]),
        ),
    ]
