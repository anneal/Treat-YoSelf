# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tys_webapp', '0005_auto_20150730_1934'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userpreference',
            old_name='next_ship_date',
            new_name='order_date',
        ),
    ]
