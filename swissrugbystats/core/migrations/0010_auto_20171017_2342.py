# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20171004_0202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalassociation',
            name='history_change_reason',
        ),
        migrations.RemoveField(
            model_name='historicalclub',
            name='history_change_reason',
        ),
        migrations.RemoveField(
            model_name='historicalcompetition',
            name='history_change_reason',
        ),
        migrations.RemoveField(
            model_name='historicalfavorite',
            name='history_change_reason',
        ),
        migrations.RemoveField(
            model_name='historicalgame',
            name='history_change_reason',
        ),
        migrations.RemoveField(
            model_name='historicalgameparticipation',
            name='history_change_reason',
        ),
        migrations.RemoveField(
            model_name='historicalleague',
            name='history_change_reason',
        ),
        migrations.RemoveField(
            model_name='historicalreferee',
            name='history_change_reason',
        ),
        migrations.RemoveField(
            model_name='historicalseason',
            name='history_change_reason',
        ),
        migrations.RemoveField(
            model_name='historicalteam',
            name='history_change_reason',
        ),
        migrations.RemoveField(
            model_name='historicalvenue',
            name='history_change_reason',
        ),
        migrations.AlterField(
            model_name='historicalassociation',
            name='history_type',
            field=models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')]),
        ),
        migrations.AlterField(
            model_name='historicalassociation',
            name='parent_association',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.Association', null=True),
        ),
        migrations.AlterField(
            model_name='historicalclub',
            name='history_type',
            field=models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')]),
        ),
        migrations.AlterField(
            model_name='historicalcompetition',
            name='history_type',
            field=models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')]),
        ),
        migrations.AlterField(
            model_name='historicalfavorite',
            name='history_type',
            field=models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')]),
        ),
        migrations.AlterField(
            model_name='historicalgame',
            name='history_type',
            field=models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')]),
        ),
        migrations.AlterField(
            model_name='historicalgameparticipation',
            name='history_type',
            field=models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')]),
        ),
        migrations.AlterField(
            model_name='historicalleague',
            name='history_type',
            field=models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')]),
        ),
        migrations.AlterField(
            model_name='historicalreferee',
            name='history_type',
            field=models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')]),
        ),
        migrations.AlterField(
            model_name='historicalseason',
            name='history_type',
            field=models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')]),
        ),
        migrations.AlterField(
            model_name='historicalteam',
            name='history_type',
            field=models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')]),
        ),
        migrations.AlterField(
            model_name='historicalvenue',
            name='history_type',
            field=models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')]),
        ),
    ]
