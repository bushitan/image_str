# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0028_userlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlog',
            name='data',
            field=models.CharField(max_length=32, null=True, verbose_name='\u6570\u636e', blank=True),
        ),
    ]
