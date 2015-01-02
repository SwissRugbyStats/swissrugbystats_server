# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swissrugby', '0004_auto_20141206_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameparticipation',
            name='points',
            field=models.IntegerField(null=True, verbose_name=b'Points', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gameparticipation',
            name='tries',
            field=models.IntegerField(null=True, verbose_name=b'Tries', blank=True),
            preserve_default=True,
        ),
    ]
