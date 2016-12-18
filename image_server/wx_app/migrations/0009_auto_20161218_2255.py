# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0008_auto_20161218_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='img',
            name='duration',
            field=models.FloatField(default=0, null=True, verbose_name=b'\xe6\x97\xb6\xe9\x95\xbf'),
        ),
        migrations.AlterField(
            model_name='img',
            name='height',
            field=models.IntegerField(default=0, null=True, verbose_name=b'\xe9\xab\x98'),
        ),
        migrations.AlterField(
            model_name='img',
            name='width',
            field=models.IntegerField(default=0, null=True, verbose_name=b'\xe5\xae\xbd'),
        ),
    ]
