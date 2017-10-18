# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-18 19:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0009_auto_20171004_0202'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.CharField(blank=True, help_text='Additional notes regarding the card, i.e. "High Tackle" or similar.', max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CardType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the card type.', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='LineUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.GameParticipation')),
            ],
        ),
        migrations.CreateModel(
            name='LineUpPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_number', models.IntegerField()),
                ('lineup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coach.LineUp')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='First name of the player.', max_length=50)),
                ('last_name', models.CharField(help_text='Last name of the player.', max_length=50)),
                ('photo', models.ImageField(blank=True, help_text='Portrait photo of the player.', null=True, upload_to='players/')),
                ('birth_date', models.DateField(blank=True, help_text='Date of birth. Used to calculate the age.', null=True)),
                ('height', models.IntegerField(blank=True, help_text='Current height of the player.', null=True)),
                ('weight', models.IntegerField(blank=True, help_text='Current weight of the player.', null=True)),
                ('club', models.ForeignKey(help_text='The main club the player belongs to.', on_delete=django.db.models.deletion.CASCADE, to='core.Club')),
            ],
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(help_text='Game during which this point has been scored.', on_delete=django.db.models.deletion.CASCADE, to='core.Game')),
                ('player', models.ForeignKey(help_text='Player who actually scored the point.', on_delete=django.db.models.deletion.CASCADE, to='coach.Player')),
            ],
        ),
        migrations.CreateModel(
            name='PointType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the point type (i.e. "Try" or "Goal")', max_length=50)),
                ('value', models.IntegerField(help_text='Numeric value of the point type (i.e. 5 for a try, 3 for a penalty)')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Substitution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_in', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_in', to='coach.Player')),
                ('player_out', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_out', to='coach.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Trophy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coach.Player')),
            ],
        ),
        migrations.CreateModel(
            name='TrophyType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the trophy, i.e. "Man of the Match" or "Tackle of the Match"', max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='trophy',
            name='trophy_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coach.TrophyType'),
        ),
        migrations.AddField(
            model_name='point',
            name='point_type',
            field=models.ForeignKey(help_text='Type of point that was made.', on_delete=django.db.models.deletion.CASCADE, to='coach.PointType'),
        ),
        migrations.AddField(
            model_name='player',
            name='default_positions',
            field=models.ManyToManyField(blank=True, help_text='The positions this player usually plays on.', to='coach.Position'),
        ),
        migrations.AddField(
            model_name='lineupposition',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coach.Player'),
        ),
        migrations.AddField(
            model_name='card',
            name='card_type',
            field=models.ForeignKey(help_text='Type of card which was received.', on_delete=django.db.models.deletion.CASCADE, to='coach.CardType'),
        ),
        migrations.AddField(
            model_name='card',
            name='game',
            field=models.ForeignKey(help_text='Game during which this card has been received.', on_delete=django.db.models.deletion.CASCADE, to='core.Game'),
        ),
        migrations.AddField(
            model_name='card',
            name='player',
            field=models.ForeignKey(help_text='Player that actually received the card.', on_delete=django.db.models.deletion.CASCADE, to='coach.Player'),
        ),
    ]
