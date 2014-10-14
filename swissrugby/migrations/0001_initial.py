# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fsrID', models.CharField(max_length=10, null=True, verbose_name=b'FSR ID', blank=True)),
                ('fsrUrl', models.CharField(max_length=100, null=True, verbose_name=b'FSR Url', blank=True)),
                ('date', models.DateTimeField(verbose_name=b'KickOff')),
                ('hostScore', models.IntegerField(null=True, verbose_name=b'Host Score', blank=True)),
                ('guestScore', models.IntegerField(null=True, verbose_name=b'Guest Score', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('shortCode', models.CharField(max_length=50)),
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
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='game',
            name='guestTeam',
            field=models.ForeignKey(related_name=b'guestTeam_set', verbose_name=b'Guest', to='swissrugby.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='hostTeam',
            field=models.ForeignKey(related_name=b'hostTeam_set', verbose_name=b'Host', to='swissrugby.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='league',
            field=models.ForeignKey(verbose_name=b'League', to='swissrugby.League'),
            preserve_default=True,
        ),
    ]
