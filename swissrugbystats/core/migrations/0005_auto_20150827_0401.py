# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150827_0239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='association',
            name='name',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='association',
            name='parent_association',
            field=models.ForeignKey(related_name='child_associations', verbose_name=b'Parent Association', blank=True, to='core.Association', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='club',
            name='associations',
            field=models.ManyToManyField(related_name='clubs', to='core.Association', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='club',
            name='website',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalassociation',
            name='name',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalclub',
            name='website',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
