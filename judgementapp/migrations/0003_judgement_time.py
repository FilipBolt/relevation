# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judgementapp', '0002_auto_20180522_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='judgement',
            name='time',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
