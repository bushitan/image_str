# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emoticon', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='parent_id',
        ),
        migrations.RemoveField(
            model_name='category',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='relcategoryimg',
            name='category',
        ),
        migrations.RemoveField(
            model_name='relcategoryimg',
            name='img',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Img',
        ),
        migrations.DeleteModel(
            name='RelCategoryImg',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
