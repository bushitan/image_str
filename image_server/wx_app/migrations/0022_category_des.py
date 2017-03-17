# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0021_auto_20170310_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='des',
            field=models.TextField(null=True, verbose_name='\u63cf\u8ff0', blank=True),
        ),
    ]
