# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0036_auto_20170711_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='tao_bao',
            field=models.CharField(max_length=100, null=True, verbose_name='\u6dd8\u5b9d\u94fe\u63a5', blank=True),
        ),
    ]
