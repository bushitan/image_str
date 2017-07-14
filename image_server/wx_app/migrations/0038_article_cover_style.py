# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0037_auto_20170711_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='cover_style',
            field=models.IntegerField(default=0, verbose_name='\u662f\u5426\u663e\u793a\u6587\u7ae0', choices=[(0, '\u56fe\u7247'), (1, '\u89c6\u9891')]),
        ),
    ]
