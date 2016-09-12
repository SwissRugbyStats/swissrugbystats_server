# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150827_0401'),
    ]

    operations = [
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
            model_name='historicalleague',
            name='shortCode',
        ),
        migrations.RemoveField(
            model_name='league',
            name='shortCode',
        ),
        migrations.AddField(
            model_name='club',
            name='description',
            field=models.TextField(help_text='Tell us something about your club.', null=True, verbose_name='Description', blank=True),
        ),
        migrations.AddField(
            model_name='club',
            name='email',
            field=models.CharField(max_length=255, null=True, verbose_name='Main E-mail', blank=True),
        ),
        migrations.AddField(
            model_name='club',
            name='facebook',
            field=models.CharField(max_length=255, null=True, verbose_name='Facebook', blank=True),
        ),
        migrations.AddField(
            model_name='club',
            name='google_plus',
            field=models.CharField(max_length=255, null=True, verbose_name='Google+', blank=True),
        ),
        migrations.AddField(
            model_name='club',
            name='instagram',
            field=models.CharField(max_length=255, null=True, verbose_name='Instagram', blank=True),
        ),
        migrations.AddField(
            model_name='club',
            name='logo',
            field=django_resized.forms.ResizedImageField(upload_to='logos/', null=True, verbose_name='Club logo', blank=True),
        ),
        migrations.AddField(
            model_name='club',
            name='twitter',
            field=models.CharField(max_length=255, null=True, verbose_name='Twitter', blank=True),
        ),
        migrations.AddField(
            model_name='historicalclub',
            name='description',
            field=models.TextField(help_text='Tell us something about your club.', null=True, verbose_name='Description', blank=True),
        ),
        migrations.AddField(
            model_name='historicalclub',
            name='email',
            field=models.CharField(max_length=255, null=True, verbose_name='Main E-mail', blank=True),
        ),
        migrations.AddField(
            model_name='historicalclub',
            name='facebook',
            field=models.CharField(max_length=255, null=True, verbose_name='Facebook', blank=True),
        ),
        migrations.AddField(
            model_name='historicalclub',
            name='google_plus',
            field=models.CharField(max_length=255, null=True, verbose_name='Google+', blank=True),
        ),
        migrations.AddField(
            model_name='historicalclub',
            name='instagram',
            field=models.CharField(max_length=255, null=True, verbose_name='Instagram', blank=True),
        ),
        migrations.AddField(
            model_name='historicalclub',
            name='logo',
            field=models.TextField(max_length=100, null=True, verbose_name='Club logo', blank=True),
        ),
        migrations.AddField(
            model_name='historicalclub',
            name='twitter',
            field=models.CharField(max_length=255, null=True, verbose_name='Twitter', blank=True),
        ),
        migrations.AddField(
            model_name='historicalleague',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalleague',
            name='shortcode',
            field=models.CharField(db_index=True, max_length=50, null=True, blank=True),
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
        migrations.AlterField(
            model_name='club',
            name='website',
            field=models.CharField(max_length=255, null=True, verbose_name='Website', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalassociation',
            name='abbreviation',
            field=models.CharField(max_length=10, db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalclub',
            name='website',
            field=models.CharField(max_length=255, null=True, verbose_name='Website', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalseason',
            name='fsr_url_slug',
            field=models.CharField(db_index=True, max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='season',
            name='fsr_url_slug',
            field=models.CharField(max_length=50, unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='club',
            field=models.ForeignKey(blank=True, to='core.Club', null=True),
        ),
    ]
