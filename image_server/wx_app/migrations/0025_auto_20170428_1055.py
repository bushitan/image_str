# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0024_auto_20170327_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='tao_bao',
            field=models.TextField(null=True, verbose_name='\u6dd8\u5b9d\u94fe\u63a5', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(null=True, verbose_name='\u6b63\u6587', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='is_show',
            field=models.IntegerField(default=1, verbose_name='\u662f\u5426\u663e\u793a\u6587\u7ae0', choices=[(0, '\u9690\u85cf'), (1, '\u663e\u793a')]),
        ),
        migrations.AlterField(
            model_name='article',
            name='summary',
            field=models.TextField(null=True, verbose_name='\u6458\u8981', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=100, null=True, verbose_name='\u6807\u9898', blank=True),
        ),
    ]
