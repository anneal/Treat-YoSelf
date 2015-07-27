# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EtsyUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('etsy_user_id', models.PositiveIntegerField(default=0)),
                ('etsy_gender', models.CharField(max_length=100, default='')),
                ('etsy_country_id', models.PositiveIntegerField(null=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('keyword', models.CharField(max_length=200, default='')),
                ('keyword_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('keyword_desc', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('listing_id', models.CharField(max_length=10, default='null')),
            ],
        ),
        migrations.AddField(
            model_name='etsyuser',
            name='listing',
            field=models.ForeignKey(null=True, blank=True, to='tys_webapp.Listing'),
        ),
        migrations.AddField(
            model_name='etsyuser',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
