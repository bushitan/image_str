# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0040_article_btn_left_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleNext',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('left_name', models.CharField(max_length=32, null=True, verbose_name='\u5de6\u8fb9\u540d\u5b57', blank=True)),
                ('right_name', models.CharField(max_length=32, null=True, verbose_name='\u53f3\u8fb9\u540d\u5b57', blank=True)),
            ],
            options={
                'verbose_name': '\u4e0b\u4e00\u7bc7\u6587\u7ae0',
                'verbose_name_plural': '\u4e0b\u4e00\u7bc7\u6587\u7ae0',
            },
        ),
        migrations.RemoveField(
            model_name='article',
            name='btn_left',
        ),
        migrations.RemoveField(
            model_name='article',
            name='btn_left_url',
        ),
        migrations.RemoveField(
            model_name='article',
            name='btn_right',
        ),
        migrations.AddField(
            model_name='articlenext',
            name='art',
            field=models.ForeignKey(verbose_name='\u6587\u7ae0', blank=True, to='wx_app.Article', null=True),
        ),
    ]
