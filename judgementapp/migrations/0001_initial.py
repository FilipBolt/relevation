# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('docId', models.CharField(max_length=250)),
                ('text', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Judgement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField(null=True, blank=True)),
                ('relevance', models.IntegerField()),
                ('annotator', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('document', models.ForeignKey(to='judgementapp.Document')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qId', models.IntegerField()),
                ('text', models.CharField(max_length=250)),
                ('difficulty', models.IntegerField(null=True, blank=True)),
                ('comment', models.TextField(null=True, blank=True)),
                ('instructions', models.TextField(null=True, blank=True)),
                ('criteria', models.TextField(null=True, blank=True)),
                ('example', models.TextField(null=True, blank=True)),
                ('annotator', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='judgement',
            name='query',
            field=models.ForeignKey(to='judgementapp.Query'),
            preserve_default=True,
        ),
    ]
