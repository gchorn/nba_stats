# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-22 04:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0004_auto_20170821_0730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='losses',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='wins',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
