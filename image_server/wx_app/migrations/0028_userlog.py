# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0027_article_cover'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.CharField(max_length=32, null=True, verbose_name='\u52a8\u4f5c', blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('user', models.ForeignKey(verbose_name='\u7528\u6237', blank=True, to='wx_app.User', null=True)),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': '\u7528\u6237\u65e5\u5fd7',
                'verbose_name_plural': '\u7528\u6237\u65e5\u5fd7',
            },
        ),
    ]
