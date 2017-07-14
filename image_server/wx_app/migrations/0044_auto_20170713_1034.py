# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0043_auto_20170713_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='cover',
            field=models.CharField(max_length=100, null=True, verbose_name='\u5c01\u9762\u56fe\u7247', blank=True),
        ),
        migrations.AddField(
            model_name='story',
            name='cover_style',
            field=models.IntegerField(default=0, verbose_name='\u5c01\u9762\u7c7b\u578b', choices=[(0, '\u56fe\u7247'), (1, '\u89c6\u9891')]),
        ),
        migrations.AddField(
            model_name='story',
            name='is_show',
            field=models.IntegerField(default=1, verbose_name='\u662f\u5426\u663e\u793a\u6587\u7ae0', choices=[(0, '\u9690\u85cf'), (1, '\u663e\u793a')]),
        ),
        migrations.AddField(
            model_name='story',
            name='summary',
            field=models.CharField(max_length=100, null=True, verbose_name='\u6458\u8981', blank=True),
        ),
        migrations.AddField(
            model_name='story',
            name='title',
            field=models.CharField(max_length=100, null=True, verbose_name='\u6807\u9898', blank=True),
        ),
    ]
