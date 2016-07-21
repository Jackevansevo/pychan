# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-15 22:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0007_auto_20160715_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='thread',
            name='image',
            field=models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='Image'),
        ),
    ]
