# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2019-08-25 08:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Wenzhai', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generation',
            name='Status',
            field=models.CharField(max_length=5),
        ),
    ]
