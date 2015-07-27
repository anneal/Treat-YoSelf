# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tys_webapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserExcludedKeyword',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('excluded_keywords', models.ForeignKey(null=True, to='tys_webapp.Keyword', blank=True)),
                ('user', models.ForeignKey(to='tys_webapp.EtsyUser')),
            ],
        ),
        migrations.CreateModel(
            name='UserIncludedKeyword',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('included_keywords', models.ForeignKey(null=True, to='tys_webapp.Keyword', blank=True)),
                ('user', models.ForeignKey(to='tys_webapp.EtsyUser')),
            ],
        ),
        migrations.CreateModel(
            name='UserPreference',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('ship_frequency', models.PositiveIntegerField(default=14)),
                ('next_ship_date', models.DateField(default=django.utils.timezone.now)),
                ('price_max', models.DecimalField(default=25.0, decimal_places=2, max_digits=8)),
                ('price_min', models.DecimalField(default=0.0, decimal_places=2, max_digits=8)),
                ('user', models.OneToOneField(to='tys_webapp.EtsyUser')),
            ],
        ),
    ]
