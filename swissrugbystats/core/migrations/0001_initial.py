# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fsrID', models.CharField(max_length=10, null=True, verbose_name=b'FSR ID', blank=True)),
                ('fsrUrl', models.CharField(max_length=100, null=True, verbose_name=b'FSR Url', blank=True)),
                ('date', models.DateTimeField(verbose_name=b'KickOff')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GameParticipation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(null=True, verbose_name=b'Score', blank=True)),
                ('tries', models.IntegerField(null=True, verbose_name=b'Tries', blank=True)),
                ('redCards', models.IntegerField(null=True, verbose_name=b'Red Cards', blank=True)),
                ('points', models.IntegerField(null=True, verbose_name=b'Points', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalFavorite',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical favorite',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalGame',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('fsrID', models.CharField(max_length=10, null=True, verbose_name=b'FSR ID', blank=True)),
                ('fsrUrl', models.CharField(max_length=100, null=True, verbose_name=b'FSR Url', blank=True)),
                ('date', models.DateTimeField(verbose_name=b'KickOff')),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('guest', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.GameParticipation', null=True)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('host', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.GameParticipation', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical game',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalGameParticipation',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('score', models.IntegerField(null=True, verbose_name=b'Score', blank=True)),
                ('tries', models.IntegerField(null=True, verbose_name=b'Tries', blank=True)),
                ('redCards', models.IntegerField(null=True, verbose_name=b'Red Cards', blank=True)),
                ('points', models.IntegerField(null=True, verbose_name=b'Points', blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical game participation',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalLeague',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('shortCode', models.CharField(max_length=50)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical league',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalReferee',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=100)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical referee',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalSeason',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical season',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalTeam',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=50)),
                ('logo', models.CharField(max_length=200, null=True, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical team',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalVenue',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=100)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical venue',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('shortCode', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Referee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('logo', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='historicalgameparticipation',
            name='team',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.Team', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalgame',
            name='league',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.League', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalgame',
            name='referee',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.Referee', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalgame',
            name='season',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.Season', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalgame',
            name='venue',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.Venue', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalfavorite',
            name='team',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.Team', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicalfavorite',
            name='user',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gameparticipation',
            name='team',
            field=models.ForeignKey(related_name='Team_set', verbose_name=b'Team', to='core.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='guest',
            field=models.ForeignKey(related_name='guestTeam_set', verbose_name=b'Guest Participation', to='core.GameParticipation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='host',
            field=models.ForeignKey(related_name='hostTeam_set', verbose_name=b'Host Participation', to='core.GameParticipation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='league',
            field=models.ForeignKey(related_name='league_games', verbose_name=b'League', to='core.League'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='referee',
            field=models.ForeignKey(verbose_name=b'Referee', blank=True, to='core.Referee', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='season',
            field=models.ForeignKey(related_name='season_games', verbose_name=b'Season', to='core.Season'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='venue',
            field=models.ForeignKey(verbose_name=b'Venue', blank=True, to='core.Venue', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='favorite',
            name='team',
            field=models.ForeignKey(related_name='Team', verbose_name=b'Team', to='core.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(related_name='Owner', verbose_name=b'User', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
