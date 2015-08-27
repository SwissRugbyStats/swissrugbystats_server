# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150827_0119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='club',
            field=models.ForeignKey(to='core.Club', null=True),
            preserve_default=True,
        ),
    ]
