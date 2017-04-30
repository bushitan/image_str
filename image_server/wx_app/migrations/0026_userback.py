# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0025_auto_20170428_1055'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('back', models.TextField(null=True, verbose_name='\u53cd\u9988\u4fe1\u606f', blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('user', models.ForeignKey(verbose_name='\u7528\u6237', blank=True, to='wx_app.User', null=True)),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': '\u7528\u6237\u53cd\u9988',
                'verbose_name_plural': '\u7528\u6237\u53cd\u9988',
            },
        ),
    ]
