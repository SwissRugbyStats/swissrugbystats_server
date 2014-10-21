# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swissrugby', '0002_auto_20141015_1149'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameParticipation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(null=True, verbose_name=b'Score', blank=True)),
                ('tries', models.IntegerField(null=True, verbose_name=b'Score', blank=True)),
                ('redCards', models.IntegerField(null=True, verbose_name=b'Red Cards', blank=True)),
                ('points', models.IntegerField(null=True, verbose_name=b'Score', blank=True)),
                ('team', models.ForeignKey(related_name=b'Team_set', verbose_name=b'Team', to='swissrugby.Team')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='game',
            name='guestScore',
        ),
        migrations.RemoveField(
            model_name='game',
            name='guestTeam',
        ),
        migrations.RemoveField(
            model_name='game',
            name='hostScore',
        ),
        migrations.RemoveField(
            model_name='game',
            name='hostTeam',
        ),
        migrations.AddField(
            model_name='game',
            name='guest',
            field=models.ForeignKey(related_name=b'guestTeam_set', default=1, verbose_name=b'Guest Participation', to='swissrugby.GameParticipation'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='host',
            field=models.ForeignKey(related_name=b'hostTeam_set', default=1, verbose_name=b'Host Participation', to='swissrugby.GameParticipation'),
            preserve_default=False,
        ),
    ]
