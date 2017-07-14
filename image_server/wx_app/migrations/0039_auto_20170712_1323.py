# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0038_article_cover_style'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='btn_left',
            field=models.CharField(max_length=32, null=True, verbose_name='\u5de6\u8fb9\u6309\u94ae', blank=True),
        ),
        migrations.AddField(
            model_name='article',
            name='btn_right',
            field=models.CharField(max_length=32, null=True, verbose_name='\u53f3\u8fb9\u6309\u94ae', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='cover_style',
            field=models.IntegerField(default=0, verbose_name='\u5c01\u9762\u7c7b\u578b', choices=[(0, '\u56fe\u7247'), (1, '\u89c6\u9891')]),
        ),
    ]
