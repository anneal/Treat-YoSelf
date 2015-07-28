# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tys_webapp', '0003_auto_20150728_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userexcludedkeyword',
            name='excluded_keywords',
            field=models.ManyToManyField(verbose_name='Treats I Like', blank=True, to='tys_webapp.Keyword', null=True),
        ),
        migrations.AlterField(
            model_name='userincludedkeyword',
            name='included_keywords',
            field=models.ManyToManyField(verbose_name='Things I                                                do NOT want', blank=True, to='tys_webapp.Keyword', null=True),
        ),
        migrations.AlterField(
            model_name='userpreference',
            name='next_ship_date',
            field=models.DateField(verbose_name='Expected Order Date', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='userpreference',
            name='price_max',
            field=models.DecimalField(verbose_name='Max Price Point', max_digits=8, default=25.0, help_text='Includes Shipping Costs', decimal_places=2),
        ),
        migrations.AlterField(
            model_name='userpreference',
            name='price_min',
            field=models.DecimalField(verbose_name='Min Price Point', max_digits=8, default=0.0, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='userpreference',
            name='ship_frequency',
            field=models.PositiveIntegerField(verbose_name="Days between                                                  Treat Yo'Self Orders", default=14),
        ),
    ]
