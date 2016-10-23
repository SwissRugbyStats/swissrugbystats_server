# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20161023_0148'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameparticipation',
            name='forfait',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalgameparticipation',
            name='forfait',
            field=models.BooleanField(default=False),
        ),
    ]
