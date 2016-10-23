# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20160912_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalteam',
            name='card_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalteam',
            name='draw_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalteam',
            name='game_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalteam',
            name='loss_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalteam',
            name='point_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalteam',
            name='try_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalteam',
            name='win_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='team',
            name='card_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='team',
            name='draw_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='team',
            name='game_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='team',
            name='loss_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='team',
            name='point_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='team',
            name='try_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='team',
            name='win_count',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
