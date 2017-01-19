# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0017_auto_20170118_2258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='step',
            name='img_id',
        ),
        migrations.AddField(
            model_name='step',
            name='img_url',
            field=models.TextField(null=True, verbose_name='\u56fe\u7247\u5730\u5740', blank=True),
        ),
        migrations.AddField(
            model_name='theme',
            name='lift',
            field=models.IntegerField(default=0, verbose_name='\u751f\u547d\u5468\u671f', choices=[(0, '\u6fc0\u6d3b'), (1, '\u4e0d\u6fc0\u6d3b'), (2, '\u5220\u9664')]),
        ),
    ]
