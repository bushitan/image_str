# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0015_auto_20170118_2059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='step',
            name='name',
        ),
        migrations.AddField(
            model_name='step',
            name='is_free',
            field=models.IntegerField(default=0, verbose_name='\u662f\u5426\u53ef\u62a2', choices=[(0, '\u7a7a\u95f2\uff0c\u53ef\u4e0b\u4e00\u6b65'), (1, '\u975e\u7a7a\u95f2\uff0c\u4e0d\u80fd\u4e0b\u4e00\u6b65')]),
        ),
        migrations.AlterField(
            model_name='step',
            name='number',
            field=models.IntegerField(default=1, null=True, verbose_name='\u6b65\u6570', blank=True),
        ),
    ]
