# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 17:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0005_auto_20170822_0441'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='api_id',
            field=models.CharField(default='', max_length=30),
        ),
    ]