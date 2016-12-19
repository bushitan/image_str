# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0010_auto_20161219_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='parent_id',
            field=models.ForeignKey(verbose_name='\u7236\u7c7b\u76ee\u5f55', to='wx_app.Category', null=True),
        ),
    ]
