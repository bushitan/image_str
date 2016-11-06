# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0003_auto_20161106_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='img',
            name='yun_url',
            field=models.TextField(null=True, verbose_name='\u4e91\u5b58\u50a8\u5730\u5740'),
        ),
    ]
