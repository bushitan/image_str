# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0018_auto_20170119_0837'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='step',
            options={'get_latest_by': 'create_time', 'verbose_name': '\u7ed8\u753b\u6b65\u9aa4', 'verbose_name_plural': '\u7ed8\u753b\u6b65\u9aa4'},
        ),
        migrations.RenameField(
            model_name='step',
            old_name='theme_id',
            new_name='theme',
        ),
        migrations.RenameField(
            model_name='step',
            old_name='user_id',
            new_name='user',
        ),
    ]
