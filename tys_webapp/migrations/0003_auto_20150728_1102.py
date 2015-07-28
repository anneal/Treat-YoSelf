# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tys_webapp', '0002_userexcludedkeyword_userincludedkeyword_userpreference'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userexcludedkeyword',
            name='excluded_keywords',
        ),
        migrations.AddField(
            model_name='userexcludedkeyword',
            name='excluded_keywords',
            field=models.ManyToManyField(blank=True, null=True, to='tys_webapp.Keyword'),
        ),
        migrations.RemoveField(
            model_name='userincludedkeyword',
            name='included_keywords',
        ),
        migrations.AddField(
            model_name='userincludedkeyword',
            name='included_keywords',
            field=models.ManyToManyField(blank=True, null=True, to='tys_webapp.Keyword'),
        ),
    ]
