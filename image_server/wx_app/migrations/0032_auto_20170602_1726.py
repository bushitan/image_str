# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0031_auto_20170602_1558'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelMasterUserImg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4', null=True)),
                ('img', models.ForeignKey(verbose_name='\u6536\u5230\u56fe\u7247', to='wx_app.Img')),
                ('user', models.ForeignKey(verbose_name='master\u7528\u6237', blank=True, to='wx_app.User', null=True)),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': '\u533f\u540d\u56de\u590d\u56fe\u7247',
                'verbose_name_plural': '\u533f\u540d\u56de\u590d\u56fe\u7247',
            },
        ),
        migrations.RemoveField(
            model_name='relmasterimg',
            name='img',
        ),
        migrations.RemoveField(
            model_name='relmasterimg',
            name='user',
        ),
        migrations.DeleteModel(
            name='RelMasterImg',
        ),
    ]
