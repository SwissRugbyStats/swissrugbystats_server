# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_resized.forms
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [(b'core', '0001_initial'), (b'core', '0002_auto_20150827_0059'), (b'core', '0003_auto_20150827_0119'), (b'core', '0004_auto_20150827_0239'), (b'core', '0005_auto_20150827_0401'), (b'core', '0006_auto_20160912_1639'), (b'core', '0007_auto_20161023_0148'), (b'core', '0008_auto_20161023_1430'), (b'core', '0009_auto_20171004_0202'), (b'core', '0010_auto_20171017_2342')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fsrID', models.CharField(max_length=10, null=True, verbose_name=b'FSR ID', blank=True)),
                ('fsrUrl', models.CharField(max_length=100, null=True, verbose_name=b'FSR Url', blank=True)),
                ('date', models.DateTimeField(verbose_name=b'KickOff')),
            ],
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
        ),
        migrations.CreateModel(
            name='HistoricalLeague',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('shortcode', models.CharField(db_index=True, max_length=50, null=True, blank=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical league',
            },
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
                ('fsr_url_slug', models.CharField(db_index=True, max_length=50, null=True, blank=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical season',
            },
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
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('shortCode', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Referee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('logo', models.CharField(max_length=200, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='historicalgameparticipation',
            name='team',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.Team', null=True),
        ),
        migrations.AddField(
            model_name='historicalgame',
            name='referee',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.Referee', null=True),
        ),
        migrations.AddField(
            model_name='historicalgame',
            name='venue',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.Venue', null=True),
        ),
        migrations.AddField(
            model_name='historicalfavorite',
            name='team',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.Team', null=True),
        ),
        migrations.AddField(
            model_name='historicalfavorite',
            name='user',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='gameparticipation',
            name='team',
            field=models.ForeignKey(related_name='Team_set', verbose_name='Team', to='core.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='guest',
            field=models.ForeignKey(related_name='guestTeam_set', verbose_name='Guest Participation', to='core.GameParticipation'),
        ),
        migrations.AddField(
            model_name='game',
            name='host',
            field=models.ForeignKey(related_name='hostTeam_set', verbose_name='Host Participation', to='core.GameParticipation'),
        ),
        migrations.AddField(
            model_name='game',
            name='referee',
            field=models.ForeignKey(verbose_name='Referee', blank=True, to='core.Referee', null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='venue',
            field=models.ForeignKey(verbose_name='Venue', blank=True, to='core.Venue', null=True),
        ),
        migrations.AddField(
            model_name='favorite',
            name='team',
            field=models.ForeignKey(related_name='Team', verbose_name='Team', to='core.Team'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(related_name='Owner', verbose_name='User', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Association',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('abbreviation', models.CharField(max_length=10)),
                ('parent_association', models.ForeignKey(related_name='child_associations', verbose_name=b'Parent Association', to='core.Association')),
            ],
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('abbreviation', models.CharField(max_length=10)),
                ('website', models.CharField(max_length=255, null=True, verbose_name='Website', blank=True)),
                ('associations', models.ManyToManyField(related_name='clubs', to=b'core.Association', blank=True)),
                ('description', models.TextField(help_text='Tell us something about your club.', null=True, verbose_name='Description', blank=True)),
                ('email', models.CharField(max_length=255, null=True, verbose_name='Main E-mail', blank=True)),
                ('facebook', models.CharField(max_length=255, null=True, verbose_name='Facebook', blank=True)),
                ('google_plus', models.CharField(max_length=255, null=True, verbose_name='Google+', blank=True)),
                ('instagram', models.CharField(max_length=255, null=True, verbose_name='Instagram', blank=True)),
                ('logo', django_resized.forms.ResizedImageField(upload_to='logos/', null=True, verbose_name='Club logo', blank=True)),
                ('twitter', models.CharField(max_length=255, null=True, verbose_name='Twitter', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('league', models.ForeignKey(related_name='league_competitions', verbose_name='League', to='core.League')),
                ('season', models.ForeignKey(related_name='season_competitions', verbose_name='Season', to='core.Season')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalAssociation',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('abbreviation', models.CharField(max_length=10, db_index=True)),
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
        ),
        migrations.CreateModel(
            name='HistoricalClub',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('abbreviation', models.CharField(max_length=10)),
                ('website', models.CharField(max_length=255, null=True, verbose_name='Website', blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('description', models.TextField(help_text='Tell us something about your club.', null=True, verbose_name='Description', blank=True)),
                ('email', models.CharField(max_length=255, null=True, verbose_name='Main E-mail', blank=True)),
                ('facebook', models.CharField(max_length=255, null=True, verbose_name='Facebook', blank=True)),
                ('google_plus', models.CharField(max_length=255, null=True, verbose_name='Google+', blank=True)),
                ('instagram', models.CharField(max_length=255, null=True, verbose_name='Instagram', blank=True)),
                ('logo', models.TextField(max_length=100, null=True, verbose_name='Club logo', blank=True)),
                ('twitter', models.CharField(max_length=255, null=True, verbose_name='Twitter', blank=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical club',
            },
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
        ),
        migrations.AddField(
            model_name='game',
            name='competition',
            field=models.ForeignKey(related_name='competition_games', verbose_name='Competition', to='core.Competition'),
        ),
        migrations.AddField(
            model_name='historicalgame',
            name='competition',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.Competition', null=True),
        ),
        migrations.AddField(
            model_name='historicalteam',
            name='club',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.Club', null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='club',
            field=models.ForeignKey(blank=True, to='core.Club', null=True),
        ),
        migrations.AddField(
            model_name='season',
            name='fsr_url_slug',
            field=models.CharField(max_length=50, unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='association',
            name='name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='association',
            name='parent_association',
            field=models.ForeignKey(related_name='child_associations', verbose_name=b'Parent Association', blank=True, to='core.Association', null=True),
        ),
        migrations.RenameField(
            model_name='historicalteam',
            old_name='logo',
            new_name='fsr_logo',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='logo',
            new_name='fsr_logo',
        ),
        migrations.RemoveField(
            model_name='league',
            name='shortCode',
        ),
        migrations.AddField(
            model_name='historicalteam',
            name='current_competition',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='core.Competition', null=True),
        ),
        migrations.AddField(
            model_name='historicalteam',
            name='custom_logo',
            field=models.TextField(help_text='Custom team logo.', max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='league',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='league',
            name='shortcode',
            field=models.CharField(max_length=50, unique=True, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='team',
            name='current_competition',
            field=models.ForeignKey(verbose_name='Aktueller Wettbewerb', blank=True, to='core.Competition', null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='custom_logo',
            field=django_resized.forms.ResizedImageField(help_text='Custom team logo.', null=True, upload_to='logos/', blank=True),
        ),
        migrations.AlterField(
            model_name='association',
            name='abbreviation',
            field=models.CharField(unique=True, max_length=10),
        ),
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
        migrations.AlterField(
            model_name='association',
            name='parent_association',
            field=models.ForeignKey(related_name='child_associations', verbose_name='Parent Association', blank=True, to='core.Association', null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='date',
            field=models.DateTimeField(verbose_name='KickOff'),
        ),
        migrations.AlterField(
            model_name='game',
            name='fsrID',
            field=models.CharField(max_length=10, null=True, verbose_name='FSR ID', blank=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='fsrUrl',
            field=models.CharField(max_length=100, null=True, verbose_name='FSR Url', blank=True),
        ),
        migrations.AlterField(
            model_name='gameparticipation',
            name='points',
            field=models.IntegerField(null=True, verbose_name='Points', blank=True),
        ),
        migrations.AlterField(
            model_name='gameparticipation',
            name='redCards',
            field=models.IntegerField(null=True, verbose_name='Red Cards', blank=True),
        ),
        migrations.AlterField(
            model_name='gameparticipation',
            name='score',
            field=models.IntegerField(null=True, verbose_name='Score', blank=True),
        ),
        migrations.AlterField(
            model_name='gameparticipation',
            name='tries',
            field=models.IntegerField(null=True, verbose_name='Tries', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalfavorite',
            name='history_type',
            field=models.CharField(max_length=1, choices=[('+', 'Erzeugt'), ('~', 'Changed'), ('-', 'Deleted')]),
        ),
        migrations.AlterField(
            model_name='historicalgame',
            name='date',
            field=models.DateTimeField(verbose_name='KickOff'),
        ),
        migrations.AlterField(
            model_name='historicalgame',
            name='fsrID',
            field=models.CharField(max_length=10, null=True, verbose_name='FSR ID', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalgame',
            name='fsrUrl',
            field=models.CharField(max_length=100, null=True, verbose_name='FSR Url', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalgame',
            name='history_type',
            field=models.CharField(max_length=1, choices=[('+', 'Erzeugt'), ('~', 'Changed'), ('-', 'Deleted')]),
        ),
        migrations.AlterField(
            model_name='historicalgameparticipation',
            name='history_type',
            field=models.CharField(max_length=1, choices=[('+', 'Erzeugt'), ('~', 'Changed'), ('-', 'Deleted')]),
        ),
        migrations.AlterField(
            model_name='historicalgameparticipation',
            name='points',
            field=models.IntegerField(null=True, verbose_name='Points', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalgameparticipation',
            name='redCards',
            field=models.IntegerField(null=True, verbose_name='Red Cards', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalgameparticipation',
            name='score',
            field=models.IntegerField(null=True, verbose_name='Score', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalgameparticipation',
            name='tries',
            field=models.IntegerField(null=True, verbose_name='Tries', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalteam',
            name='history_type',
            field=models.CharField(max_length=1, choices=[('+', 'Erzeugt'), ('~', 'Changed'), ('-', 'Deleted')]),
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
            model_name='historicalteam',
            name='history_type',
            field=models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')]),
        ),
    ]
