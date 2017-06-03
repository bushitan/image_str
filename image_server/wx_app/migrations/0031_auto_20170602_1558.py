# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0030_auto_20170602_1508'),
    ]

    operations = [
        migrations.CreateModel(
            name='Master',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, null=True, verbose_name='\u6807\u9898', blank=True)),
                ('logo_url', models.TextField(null=True, verbose_name='\u5934\u50cficon', blank=True)),
                ('prize_url', models.TextField(null=True, verbose_name='\u5956\u52b1\u56fe\u7247', blank=True)),
                ('is_gather_open', models.IntegerField(default=1, verbose_name='\u662f\u5426\u63a5\u53d7\u6c42\u56fe', choices=[(0, '\u5173\u95ed\uff0c\u4e0d\u63a5\u53d7\u6c42\u56fe'), (1, '\u6253\u5f00\uff0c\u53ef\u4ee5\u6c42\u56fe')])),
                ('user', models.ForeignKey(verbose_name='master\u7528\u6237', blank=True, to='wx_app.User', null=True)),
            ],
            options={
                'verbose_name': '\u53d1\u5e16\u8005',
                'verbose_name_plural': '\u53d1\u5e16\u8005',
            },
        ),
        migrations.CreateModel(
            name='RelMasterImg',
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
            model_name='masteruserimg',
            name='img',
        ),
        migrations.RemoveField(
            model_name='masteruserimg',
            name='user',
        ),
        migrations.DeleteModel(
            name='MasterUserImg',
        ),
    ]
