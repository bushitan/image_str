# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0020_auto_20170119_1117'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='step',
            options={'ordering': ['-create_time'], 'get_latest_by': 'create_time', 'verbose_name': '\u7ed8\u753b\u6b65\u9aa4', 'verbose_name_plural': '\u7ed8\u753b\u6b65\u9aa4'},
        ),
        migrations.AddField(
            model_name='category',
            name='sn',
            field=models.IntegerField(default=0, null=True, verbose_name='\u6392\u5e8f\u53f7', blank=True),
        ),
    ]
