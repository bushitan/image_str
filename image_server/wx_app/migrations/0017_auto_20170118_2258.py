# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0016_auto_20170118_2154'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='relthemeuser',
            options={'ordering': ['-create_time'], 'verbose_name': '\u7ed8\u753b\u4e3b\u9898\u4e0e\u53c2\u4e0e\u7528\u6237\u5173\u7cfb', 'verbose_name_plural': '\u7ed8\u753b\u4e3b\u9898\u4e0e\u53c2\u4e0e\u7528\u6237\u5173\u7cfb'},
        ),
        migrations.RemoveField(
            model_name='step',
            name='is_free',
        ),
        migrations.AddField(
            model_name='step',
            name='next_user',
            field=models.IntegerField(null=True, verbose_name='\u4e0b\u4e00\u4e2a\u7528\u6237', blank=True),
        ),
    ]
