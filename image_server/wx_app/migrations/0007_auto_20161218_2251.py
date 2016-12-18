# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0006_auto_20161110_1907'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('info', models.CharField(max_length=100, null=True, verbose_name='\u4fe1\u606f')),
                ('level', models.IntegerField(default=0, verbose_name='\u4fe1\u606f\u7b49\u7ea7', choices=[(0, 'log'), (1, 'info'), (2, 'warm'), (3, 'error')])),
                ('event', models.CharField(max_length=100, null=True, verbose_name='\u4fe1\u606f')),
                ('occur_time', models.DateTimeField(auto_now_add=True, verbose_name='\u53d1\u751f\u65f6\u95f4')),
                ('user', models.ForeignKey(verbose_name='\u7528\u6237', to='wx_app.User')),
            ],
        ),
        migrations.AddField(
            model_name='img',
            name='duration',
            field=models.FloatField(default=0, verbose_name=b'\xe6\x97\xb6\xe9\x95\xbf'),
        ),
        migrations.AddField(
            model_name='img',
            name='height',
            field=models.IntegerField(default=0, verbose_name=b'\xe9\xab\x98'),
        ),
        migrations.AddField(
            model_name='img',
            name='width',
            field=models.IntegerField(default=0, verbose_name=b'\xe5\xae\xbd'),
        ),
        migrations.AlterField(
            model_name='category',
            name='user_id',
            field=models.ForeignKey(verbose_name='\u7528\u6237', to='wx_app.User'),
        ),
    ]
