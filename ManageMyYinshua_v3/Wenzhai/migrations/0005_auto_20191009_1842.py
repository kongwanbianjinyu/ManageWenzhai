# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2019-10-09 10:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Wenzhai', '0004_generation_remainprintnum'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='PrintNum',
        ),
        migrations.AddField(
            model_name='label',
            name='PrintNum',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]