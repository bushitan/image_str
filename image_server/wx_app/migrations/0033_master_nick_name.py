# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0032_auto_20170602_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='master',
            name='nick_name',
            field=models.CharField(max_length=32, null=True, verbose_name='\u6635\u79f0', blank=True),
        ),
    ]
