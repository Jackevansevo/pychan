# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-17 19:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0004_auto_20161016_1941'),
    ]

    operations = [
        migrations.RenameField(
            model_name='thread',
            old_name='image',
            new_name='picture',
        ),
    ]