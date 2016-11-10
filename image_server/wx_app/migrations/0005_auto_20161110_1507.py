# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0004_auto_20161106_1441'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='wx_code',
        ),
        migrations.AddField(
            model_name='user',
            name='expires',
            field=models.CharField(max_length=50, null=True, verbose_name='Django\u7684session\u8fc7\u671f\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='user',
            name='session',
            field=models.CharField(max_length=50, null=True, verbose_name='Django\u7684session'),
        ),
        migrations.AddField(
            model_name='user',
            name='wx_expires_in',
            field=models.CharField(max_length=50, null=True, verbose_name='\u5fae\u4fe1SessionKey\u8fc7\u671f\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='user',
            name='wx_session_key',
            field=models.CharField(max_length=50, null=True, verbose_name='\u5fae\u4fe1SessionKey'),
        ),
        migrations.AlterField(
            model_name='user',
            name='wx_open_id',
            field=models.CharField(max_length=50, null=True, verbose_name='\u5fae\u4fe1OpenID'),
        ),
    ]
