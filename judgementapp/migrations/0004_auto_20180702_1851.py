# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judgementapp', '0003_judgement_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='description',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='query',
            name='narrative',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
