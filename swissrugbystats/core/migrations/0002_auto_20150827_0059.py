# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Association',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('abbreviation', models.CharField(max_length=10)),
                ('parent_association', models.ForeignKey(related_name='child_associations', verbose_name=b'Parent Association', to='core.Association')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('abbreviation', models.CharField(max_length=10)),
                ('website', models.CharField(max_length=255, null=True)),
                ('associations', models.ManyToManyField(related_name='clubs', to='core.Association')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('league', models.ForeignKey(related_name='league_competitions', verbose_name=b'League', to='core.League')),
                ('season', models.ForeignKey(related_name='season_competitions', verbose_name=b'Season', to='core.Season')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalAssociation',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('abbreviation', models.CharField(max_length=10)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('parent_association', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.Association', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical association',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalClub',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('abbreviation', models.CharField(max_length=10)),
                ('website', models.CharField(max_length=255, null=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical club',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalCompetition',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('league', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.League', null=True)),
                ('season', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.Season', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical competition',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='game',
            name='league',
        ),
        migrations.RemoveField(
            model_name='game',
            name='season',
        ),
        migrations.RemoveField(
            model_name='historicalgame',
            name='league',
        ),
        migrations.RemoveField(
            model_name='historicalgame',
            name='season',
        ),
        migrations.AddField(
            model_name='game',
            name='competition',
            field=models.ForeignKey(related_name='competition_games', default=1, verbose_name=b'Competition', to='core.Competition'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalgame',
            name='competition',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.Competition', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalteam',
            name='club',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.Club', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='team',
            name='club',
            field=models.ForeignKey(default=1, to='core.Club'),
            preserve_default=False,
        ),
    ]
