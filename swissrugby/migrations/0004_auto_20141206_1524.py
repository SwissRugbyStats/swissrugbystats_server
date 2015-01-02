# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swissrugby', '0003_auto_20141021_1134'),
    ]

    operations = [
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
            model_name='game',
            name='referee',
            field=models.ForeignKey(verbose_name=b'Referee', blank=True, to='swissrugby.Referee', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='venue',
            field=models.ForeignKey(verbose_name=b'Venue', blank=True, to='swissrugby.Venue', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='team',
            name='logo',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
