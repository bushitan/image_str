# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0039_auto_20170712_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='btn_left_url',
            field=models.ForeignKey(verbose_name='\u5de6\u8fb9\u94fe\u63a5', blank=True, to='wx_app.Article', null=True),
        ),
    ]
