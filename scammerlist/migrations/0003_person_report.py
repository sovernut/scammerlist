# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-23 17:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scammerlist', '0002_auto_20170411_0927'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='report',
            field=models.BooleanField(default=False),
        ),
    ]