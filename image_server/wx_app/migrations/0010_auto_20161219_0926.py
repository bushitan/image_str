# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0009_auto_20161218_2255'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='log',
            options={'verbose_name': '\u65e5\u5fd7', 'verbose_name_plural': '\u65e5\u5fd7'},
        ),
        migrations.AlterField(
            model_name='category',
            name='user_id',
            field=models.ForeignKey(verbose_name='\u7528\u6237', to='wx_app.User', null=True),
        ),
    ]
