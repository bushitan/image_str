# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0044_auto_20170713_1034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='tao_bao',
        ),
    ]
