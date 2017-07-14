# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0035_remove_master_qr_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='summary',
            field=models.CharField(max_length=100, null=True, verbose_name='\u6458\u8981', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='swiper',
            field=models.CharField(max_length=200, null=True, verbose_name='\u8f6e\u64ad\u56fe', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='tao_bao',
            field=models.TextField(max_length=100, null=True, verbose_name='\u6dd8\u5b9d\u94fe\u63a5', blank=True),
        ),
        migrations.AlterField(
            model_name='master',
            name='logo_url',
            field=models.TextField(default=b'', null=True, verbose_name='\u5934\u50cficon', blank=True),
        ),
        migrations.AlterField(
            model_name='master',
            name='nick_name',
            field=models.CharField(default=b'', max_length=32, null=True, verbose_name='\u6635\u79f0', blank=True),
        ),
        migrations.AlterField(
            model_name='master',
            name='prize_url',
            field=models.TextField(default=b'', null=True, verbose_name='\u5956\u52b1\u56fe\u7247', blank=True),
        ),
        migrations.AlterField(
            model_name='master',
            name='title',
            field=models.CharField(default=b'', max_length=100, null=True, verbose_name='\u6807\u9898', blank=True),
        ),
    ]
