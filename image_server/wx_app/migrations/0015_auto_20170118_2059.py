# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wx_app', '0014_img_fsize'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelThemeUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4', null=True)),
            ],
            options={
                'verbose_name': '\u7ed8\u753b\u4e3b\u9898\u4e0e\u53c2\u4e0e\u7528\u6237\u5173\u7cfb',
                'verbose_name_plural': '\u7ed8\u753b\u4e3b\u9898\u4e0e\u53c2\u4e0e\u7528\u6237\u5173\u7cfb',
            },
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, verbose_name='\u540d\u79f0', blank=True)),
                ('number', models.IntegerField(null=True, verbose_name='\u6b65\u6570', blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4', null=True)),
                ('img_id', models.ForeignKey(verbose_name='\u56fe\u7247', blank=True, to='wx_app.Img', null=True)),
            ],
            options={
                'verbose_name': '\u7ed8\u753b\u6b65\u9aa4',
                'verbose_name_plural': '\u7ed8\u753b\u6b65\u9aa4',
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, verbose_name='\u540d\u79f0', blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4', null=True)),
                ('user_id', models.ForeignKey(verbose_name='\u53d1\u8d77\u7528\u6237', blank=True, to='wx_app.User', null=True)),
            ],
            options={
                'verbose_name': '\u7ed8\u753b\u4e3b\u9898',
                'verbose_name_plural': '\u7ed8\u753b\u4e3b\u9898',
            },
        ),
        migrations.AddField(
            model_name='step',
            name='theme_id',
            field=models.ForeignKey(verbose_name='\u4e3b\u9898', blank=True, to='wx_app.Theme', null=True),
        ),
        migrations.AddField(
            model_name='step',
            name='user_id',
            field=models.ForeignKey(verbose_name='\u53c2\u4e0e\u7528\u6237', blank=True, to='wx_app.User', null=True),
        ),
        migrations.AddField(
            model_name='relthemeuser',
            name='theme',
            field=models.ForeignKey(verbose_name='\u4e3b\u9898', to='wx_app.Theme'),
        ),
        migrations.AddField(
            model_name='relthemeuser',
            name='user',
            field=models.ForeignKey(verbose_name='\u53c2\u4e0e\u7528\u6237', to='wx_app.User'),
        ),
    ]
