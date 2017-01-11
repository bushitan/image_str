# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0011_auto_20161219_1342'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='img',
            options={'ordering': ['-create_time'], 'verbose_name': '\u56fe\u7247', 'verbose_name_plural': '\u56fe\u7247'},
        ),
        migrations.AlterModelOptions(
            name='relcategoryimg',
            options={'ordering': ['-create_time'], 'verbose_name': '\u76ee\u5f55\u56fe\u7247\u5173\u7cfb', 'verbose_name_plural': '\u76ee\u5f55\u56fe\u7247\u5173\u7cfb'},
        ),
        migrations.AddField(
            model_name='category',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4', null=True),
        ),
        migrations.AddField(
            model_name='relcategoryimg',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4', null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, null=True, verbose_name='\u540d\u79f0', blank=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent_id',
            field=models.ForeignKey(verbose_name='\u7236\u7c7b\u76ee\u5f55', blank=True, to='wx_app.Category', null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='user_id',
            field=models.ForeignKey(verbose_name='\u7528\u6237', blank=True, to='wx_app.User', null=True),
        ),
        migrations.AlterField(
            model_name='img',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4', null=True),
        ),
        migrations.AlterField(
            model_name='img',
            name='duration',
            field=models.FloatField(default=0, null=True, verbose_name=b'\xe6\x97\xb6\xe9\x95\xbf', blank=True),
        ),
        migrations.AlterField(
            model_name='img',
            name='height',
            field=models.IntegerField(default=0, null=True, verbose_name=b'\xe9\xab\x98', blank=True),
        ),
        migrations.AlterField(
            model_name='img',
            name='name',
            field=models.CharField(max_length=100, null=True, verbose_name='\u540d\u79f0', blank=True),
        ),
        migrations.AlterField(
            model_name='img',
            name='width',
            field=models.IntegerField(default=0, null=True, verbose_name=b'\xe5\xae\xbd', blank=True),
        ),
        migrations.AlterField(
            model_name='img',
            name='yun_url',
            field=models.TextField(null=True, verbose_name='\u4e91\u5b58\u50a8\u5730\u5740', blank=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='event',
            field=models.CharField(max_length=100, null=True, verbose_name='\u6240\u5c5e\u4e8b\u4ef6', blank=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='info',
            field=models.CharField(max_length=100, null=True, verbose_name='\u4fe1\u606f', blank=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='user',
            field=models.ForeignKey(verbose_name='\u7528\u6237', blank=True, to='wx_app.User', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='expires',
            field=models.FloatField(null=True, verbose_name='Django\u7684session\u8fc7\u671f\u65f6\u95f4', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=100, null=True, verbose_name='\u540d\u79f0', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='session',
            field=models.CharField(max_length=128, null=True, verbose_name='Django\u7684session', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.CharField(max_length=32, null=True, verbose_name='uuid\u6807\u8bc6', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='wx_expires_in',
            field=models.FloatField(null=True, verbose_name='\u5fae\u4fe1SessionKey\u8fc7\u671f\u65f6\u95f4', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='wx_open_id',
            field=models.CharField(max_length=50, null=True, verbose_name='\u5fae\u4fe1OpenID', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='wx_session_key',
            field=models.CharField(max_length=128, null=True, verbose_name='\u5fae\u4fe1SessionKey', blank=True),
        ),
    ]
