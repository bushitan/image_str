# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0013_img_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='img',
            name='fsize',
            field=models.IntegerField(default=0, null=True, verbose_name=b'\xe6\x96\x87\xe4\xbb\xb6\xe5\xa4\xa7\xe5\xb0\x8f', blank=True),
        ),
    ]
