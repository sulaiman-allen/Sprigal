# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-10 00:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='rfid',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
