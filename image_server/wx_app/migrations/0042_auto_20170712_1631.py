# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0041_auto_20170712_1556'),
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, null=True, verbose_name='\u6545\u4e8b\u540d\u5b57', blank=True)),
                ('tree', models.TextField(null=True, verbose_name='\u5267\u60c5\u6811', blank=True)),
            ],
            options={
                'verbose_name': '\u6545\u4e8b\u5267\u60c5',
                'verbose_name_plural': '\u6545\u4e8b\u5267\u60c5',
            },
        ),
        migrations.RemoveField(
            model_name='articlenext',
            name='art',
        ),
        migrations.DeleteModel(
            name='ArticleNext',
        ),
    ]
