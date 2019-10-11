# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2019-08-25 07:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BookNumber', models.CharField(max_length=10)),
                ('BookName', models.CharField(max_length=100)),
                ('PrintNum', models.IntegerField()),
                ('Create_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Generation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GenerationNumber', models.CharField(max_length=2)),
                ('Contain', models.FloatField()),
                ('Status', models.CharField(max_length=1)),
                ('Sign', models.CharField(max_length=5)),
                ('AlreadyPrintNum', models.IntegerField()),
                ('Create_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LabelName', models.CharField(max_length=100)),
                ('AllGenerationNum', models.IntegerField()),
                ('ShowGenerationNum', models.FloatField()),
                ('Create_time', models.DateTimeField(auto_now=True)),
                ('Book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Wenzhai.Book')),
            ],
        ),
        migrations.AddField(
            model_name='generation',
            name='Label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Wenzhai.Label'),
        ),
        migrations.AlterUniqueTogether(
            name='label',
            unique_together=set([('Book', 'LabelName')]),
        ),
        migrations.AlterUniqueTogether(
            name='generation',
            unique_together=set([('Label', 'GenerationNumber')]),
        ),
    ]