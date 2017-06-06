# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0034_master_qr_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='master',
            name='qr_url',
        ),
    ]
