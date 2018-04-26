# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-20 07:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Asset', '0003_auto_20180420_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetrecord',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='UserAccess.MyUser', verbose_name='\u4f7f\u7528\u8005'),
        ),
        migrations.AlterField(
            model_name='assetrecord',
            name='record_time',
            field=models.DateField(blank=True, null=True, verbose_name='\u65f6\u95f4\u8bb0\u5f55'),
        ),
    ]
