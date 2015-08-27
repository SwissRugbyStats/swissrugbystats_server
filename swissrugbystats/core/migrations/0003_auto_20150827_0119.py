# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150827_0059'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalseason',
            name='fsr_url_slug',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='season',
            name='fsr_url_slug',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
    ]
