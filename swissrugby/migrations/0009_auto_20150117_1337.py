# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swissrugby', '0008_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='league',
            field=models.ForeignKey(related_name='league_games', verbose_name=b'League', to='swissrugby.League'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='season',
            field=models.ForeignKey(related_name='season_games', verbose_name=b'Season', to='swissrugby.Season'),
            preserve_default=True,
        ),
    ]
