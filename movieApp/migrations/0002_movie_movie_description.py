# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-25 11:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movieApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='movie_description',
            field=models.TextField(default='blah blah blah'),
            preserve_default=False,
        ),
    ]
