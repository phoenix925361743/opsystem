# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-20 06:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('UserAccess', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='\u540d\u79f0')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='\u63cf\u8ff0')),
            ],
            options={
                'verbose_name': '\u533a\u57df',
                'verbose_name_plural': '\u533a\u57df\u7ba1\u7406\u8868',
            },
        ),
        migrations.CreateModel(
            name='AssetManagement',
            fields=[
                ('asset_number', models.IntegerField(primary_key=True, serialize=False, verbose_name='\u8d44\u4ea7\u7f16\u53f7')),
                ('name', models.CharField(max_length=200, verbose_name='\u8d44\u4ea7\u540d\u79f0')),
                ('create_time', models.DateField(auto_now_add=True, verbose_name='\u521b\u5efa\u65e5\u671f')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='\u63cf\u8ff0\u8bf4\u660e')),
                ('depart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserAccess.Department', verbose_name='\u6240\u5c5e\u90e8\u95e8')),
            ],
            options={
                'verbose_name': '\u90e8\u95e8\u8d44\u4ea7',
                'verbose_name_plural': '\u90e8\u95e8\u8d44\u4ea7\u7ba1\u7406\u8868',
            },
        ),
        migrations.CreateModel(
            name='AssetProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': '\u8d44\u4ea7\u5c5e\u6027',
                'verbose_name_plural': '\u8d44\u4ea7\u5c5e\u6027\u6620\u5c04\u8868',
            },
        ),
        migrations.CreateModel(
            name='AssetRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_time', models.DateField(auto_now_add=True, verbose_name='\u65f6\u95f4\u8bb0\u5f55')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='\u4f7f\u7528\u8bf4\u660e')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asset.AssetManagement', verbose_name='\u5173\u8054\u8d44\u4ea7')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserAccess.MyUser', verbose_name='\u4f7f\u7528\u8005')),
            ],
            options={
                'ordering': ['-record_time'],
                'verbose_name': '\u4f7f\u7528\u8bb0\u5f55',
                'verbose_name_plural': '\u4f7f\u7528\u8bb0\u5f55\u7ba1\u7406\u8868',
            },
        ),
        migrations.CreateModel(
            name='IPManagement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(unique=True, verbose_name='IP\u5730\u5740')),
                ('prefix', models.IntegerField(verbose_name='\u5b50\u7f51\u4f4d\u6570')),
                ('gateway', models.GenericIPAddressField(blank=True, null=True, verbose_name='\u7f51\u5173')),
                ('allocate_time', models.DateField(blank=True, null=True, verbose_name='\u5206\u914d\u65f6\u95f4')),
                ('end_time', models.DateField(blank=True, null=True, verbose_name='\u56de\u6536\u65f6\u95f4')),
                ('usage', models.TextField(blank=True, null=True, verbose_name='\u7528\u9014')),
                ('area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Asset.Area', verbose_name='\u5206\u914d\u533a\u57df')),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='UserAccess.MyUser', verbose_name='\u4f7f\u7528\u8005')),
            ],
            options={
                'verbose_name': 'IP\u5730\u5740',
                'verbose_name_plural': 'IP\u5730\u5740\u7ba1\u7406\u8868',
            },
        ),
        migrations.CreateModel(
            name='IpStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=200, unique=True, verbose_name='\u72b6\u6001')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='\u63cf\u8ff0')),
            ],
            options={
                'verbose_name': 'ip\u72b6\u6001',
                'verbose_name_plural': 'ip\u72b6\u6001\u7ba1\u7406\u8868',
            },
        ),
        migrations.CreateModel(
            name='LifeCycle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_time', models.DateField(blank=True, null=True, verbose_name='\u91c7\u8d2d\u65f6\u95f4')),
                ('storage_time', models.DateField(blank=True, null=True, verbose_name='\u5165\u5e93\u65f6\u95f4')),
                ('use_time', models.DateField(blank=True, null=True, verbose_name='\u4f7f\u7528\u65f6\u95f4')),
                ('scrap_time', models.DateField(blank=True, null=True, verbose_name='\u62a5\u5e9f\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u751f\u547d\u5468\u671f',
                'verbose_name_plural': '\u751f\u547d\u5468\u671f\u7ba1\u7406\u8868',
            },
        ),
        migrations.CreateModel(
            name='PropertyName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='\u540d\u79f0')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='\u63cf\u8ff0\u8bf4\u660e')),
            ],
            options={
                'verbose_name': '\u8d44\u4ea7\u540d\u79f0',
                'verbose_name_plural': '\u8d44\u4ea7\u540d\u79f0\u7ba1\u7406\u8868',
            },
        ),
        migrations.CreateModel(
            name='PropertyValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=200, unique=True, verbose_name='\u5c5e\u6027\u503c')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='\u63cf\u8ff0\u8bf4\u660e')),
            ],
            options={
                'verbose_name': '\u8d44\u4ea7\u5c5e\u6027',
                'verbose_name_plural': '\u8d44\u4ea7\u5c5e\u6027\u7ba1\u7406\u8868',
            },
        ),
        migrations.CreateModel(
            name='UseType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='\u7c7b\u578b\u540d\u79f0')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='\u63cf\u8ff0\u8bf4\u660e')),
            ],
            options={
                'verbose_name': '\u4f7f\u7528\u7c7b\u578b',
                'verbose_name_plural': '\u4f7f\u7528\u7c7b\u578b\u7ba1\u7406\u8868',
            },
        ),
        migrations.AddField(
            model_name='ipmanagement',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asset.IpStatus', verbose_name='\u72b6\u6001'),
        ),
        migrations.AddField(
            model_name='assetrecord',
            name='use_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asset.UseType', verbose_name='\u4f7f\u7528\u7c7b\u578b'),
        ),
        migrations.AddField(
            model_name='assetproperty',
            name='property_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asset.PropertyName', verbose_name='\u8d44\u4ea7\u540d\u79f0'),
        ),
        migrations.AddField(
            model_name='assetproperty',
            name='property_value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asset.PropertyValue', verbose_name='\u8d44\u4ea7\u5c5e\u6027'),
        ),
        migrations.AddField(
            model_name='assetmanagement',
            name='life_cycle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Asset.LifeCycle', verbose_name='\u751f\u547d\u5468\u671f'),
        ),
        migrations.AddField(
            model_name='assetmanagement',
            name='property',
            field=models.ManyToManyField(to='Asset.AssetProperty', verbose_name='\u8d44\u4ea7\u5c5e\u6027'),
        ),
    ]
