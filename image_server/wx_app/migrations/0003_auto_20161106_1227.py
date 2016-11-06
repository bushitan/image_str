# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0002_auto_20161106_0052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='mirror',
        ),
        migrations.AddField(
            model_name='category',
            name='is_default',
            field=models.IntegerField(default=0, verbose_name='\u662f\u5426\u7528\u6237\u9ed8\u8ba4\u76ee\u5f55', choices=[(0, '\u666e\u901a\u76ee\u5f55'), (1, '\u9ed8\u8ba4\u76ee\u5f55')]),
        ),
        migrations.AddField(
            model_name='user',
            name='wx_open_id',
            field=models.CharField(max_length=32, null=True, verbose_name='\u5fae\u4fe1OpenID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_public',
            field=models.IntegerField(default=0, verbose_name='\u662f\u5426\u7ba1\u7406\u5458', choices=[(0, '\u666e\u901a\u7528\u6237'), (1, '\u7ba1\u7406\u8005')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='wx_code',
            field=models.CharField(max_length=32, null=True, verbose_name='\u5fae\u4fe1code\u7801'),
        ),
    ]
