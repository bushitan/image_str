# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0023_article'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-create_time'], 'verbose_name': '\u6587\u7ae0', 'verbose_name_plural': '\u6587\u7ae0'},
        ),
        migrations.RemoveField(
            model_name='article',
            name='en_title',
        ),
        migrations.RemoveField(
            model_name='article',
            name='img',
        ),
        migrations.RemoveField(
            model_name='article',
            name='is_top',
        ),
        migrations.RemoveField(
            model_name='article',
            name='pub_time',
        ),
        migrations.RemoveField(
            model_name='article',
            name='rank',
        ),
        migrations.RemoveField(
            model_name='article',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='article',
            name='update_time',
        ),
        migrations.RemoveField(
            model_name='article',
            name='view_times',
        ),
        migrations.RemoveField(
            model_name='article',
            name='zan_times',
        ),
        migrations.AddField(
            model_name='article',
            name='is_show',
            field=models.IntegerField(default=1, verbose_name='\u662f\u5426\u663e\u793a\u6587\u7ae0', choices=[(0, '\u5f71\u85cf'), (1, '\u663e\u793a')]),
        ),
        migrations.AddField(
            model_name='article',
            name='swiper',
            field=models.TextField(null=True, verbose_name='\u8f6e\u64ad\u56fe', blank=True),
        ),
    ]
