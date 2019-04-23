# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-03-23 08:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('axfproject', '0008_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userAccount', models.CharField(max_length=20)),
                ('productid', models.CharField(max_length=10)),
                ('productnum', models.IntegerField()),
                ('productprice', models.CharField(max_length=10)),
                ('isChose', models.BooleanField(default=True)),
                ('productimg', models.CharField(max_length=150)),
                ('productname', models.CharField(max_length=100)),
                ('orderid', models.CharField(default='0', max_length=20)),
                ('isDelete', models.BooleanField(default=False)),
            ],
        ),
    ]