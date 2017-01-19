# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0019_auto_20170119_1108'),
    ]

    operations = [
        migrations.RenameField(
            model_name='step',
            old_name='theme',
            new_name='theme_id',
        ),
        migrations.RenameField(
            model_name='step',
            old_name='user',
            new_name='user_id',
        ),
    ]
