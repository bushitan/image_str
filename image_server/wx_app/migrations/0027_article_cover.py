# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0026_userback'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='cover',
            field=models.CharField(max_length=100, null=True, verbose_name='\u5c01\u9762\u56fe\u7247', blank=True),
        ),
    ]
