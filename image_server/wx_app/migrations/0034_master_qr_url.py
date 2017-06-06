# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0033_master_nick_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='master',
            name='qr_url',
            field=models.CharField(max_length=100, null=True, verbose_name='\u4e8c\u7ef4\u7801\u56fe\u7247', blank=True),
        ),
    ]
