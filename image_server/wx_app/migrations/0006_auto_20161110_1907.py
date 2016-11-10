# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0005_auto_20161110_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='expires',
            field=models.FloatField(null=True, verbose_name='Django\u7684session\u8fc7\u671f\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='user',
            name='session',
            field=models.CharField(max_length=128, null=True, verbose_name='Django\u7684session'),
        ),
        migrations.AlterField(
            model_name='user',
            name='wx_expires_in',
            field=models.FloatField(null=True, verbose_name='\u5fae\u4fe1SessionKey\u8fc7\u671f\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='user',
            name='wx_session_key',
            field=models.CharField(max_length=128, null=True, verbose_name='\u5fae\u4fe1SessionKey'),
        ),
    ]
