# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0042_auto_20170712_1631'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='story',
            options={'ordering': ['-create_time'], 'verbose_name': '\u6545\u4e8b\u5267\u60c5', 'verbose_name_plural': '\u6545\u4e8b\u5267\u60c5'},
        ),
        migrations.AddField(
            model_name='story',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4', null=True),
        ),
    ]
