# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('status', models.SmallIntegerField(verbose_name='商品状态', default=1, choices=[(0, '下架'), (1, '上架')])),
                ('detail', tinymce.models.HTMLField(verbose_name='商品详情')),
            ],
            options={
                'verbose_name': '商品',
                'db_table': 'df_goods',
                'verbose_name_plural': '商品',
            },
        ),
    ]
