# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0012_auto_20170111_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='img',
            name='user_id',
            field=models.ForeignKey(verbose_name='\u7528\u6237', blank=True, to='wx_app.User', null=True),
        ),
    ]
