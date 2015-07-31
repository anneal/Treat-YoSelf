# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tys_webapp', '0004_auto_20150728_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='etsyuser',
            name='access_token',
            field=models.CharField(null=True, max_length=200),
        ),
        migrations.AddField(
            model_name='etsyuser',
            name='access_token_secret',
            field=models.CharField(null=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='userexcludedkeyword',
            name='excluded_keywords',
            field=models.ManyToManyField(blank=True, to='tys_webapp.Keyword', verbose_name='Things I Like'),
        ),
        migrations.AlterField(
            model_name='userincludedkeyword',
            name='included_keywords',
            field=models.ManyToManyField(blank=True, to='tys_webapp.Keyword', verbose_name='Things I                                                do NOT want'),
        ),
    ]
