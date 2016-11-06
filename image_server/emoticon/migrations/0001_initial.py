# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, verbose_name='\u540d\u79f0')),
                ('parent_id', models.OneToOneField(null=True, verbose_name='\u7236\u7c7b\u76ee\u5f55', to='emoticon.Category')),
            ],
            options={
                'verbose_name': '\u76ee\u5f55',
                'verbose_name_plural': '\u76ee\u5f55',
            },
        ),
        migrations.CreateModel(
            name='Img',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, verbose_name='\u540d\u79f0')),
                ('qiniu_url', models.DateField(null=True, verbose_name='\u4e03\u725b\u4e91\u5730\u5740')),
                ('size', models.IntegerField(default=170, verbose_name=b'\xe9\xab\x98x\xe5\xae\xbd\xe6\x9c\x80\xe5\xa4\xa7\xe5\x80\xbc')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u56fe\u7247',
                'verbose_name_plural': '\u56fe\u7247',
            },
        ),
        migrations.CreateModel(
            name='RelCategoryImg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.ForeignKey(verbose_name='\u76ee\u5f55', to='emoticon.Category')),
                ('img', models.ForeignKey(verbose_name='\u56fe\u7247', to='emoticon.Img')),
            ],
            options={
                'verbose_name': '\u76ee\u5f55\u56fe\u7247\u5173\u7cfb',
                'verbose_name_plural': '\u76ee\u5f55\u56fe\u7247\u5173\u7cfb',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, verbose_name='\u540d\u79f0')),
                ('wx_code', models.DateField(null=True, verbose_name='\u5fae\u4fe1\u5e8f\u5217\u53f7')),
                ('is_public', models.IntegerField(default=0, verbose_name='\u662f\u5426\u516c\u5171\u7528\u6237', choices=[(0, '\u666e\u901a\u7528\u6237'), (1, '\u7ba1\u7406\u8005')])),
                ('uuid', models.CharField(max_length=32, null=True, verbose_name='uuid\u6807\u8bc6')),
                ('mirror', models.TextField(null=True, verbose_name='\u9274', blank=True)),
            ],
            options={
                'verbose_name': '\u7528\u6237',
                'verbose_name_plural': '\u7528\u6237',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='user_id',
            field=models.ForeignKey(verbose_name='\u76ee\u5f55', to='emoticon.User'),
        ),
    ]
