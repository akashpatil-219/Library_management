# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-30 13:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_books'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='user_type',
            field=models.CharField(choices=[('student', 'Student'), ('librarian', 'Librarian')], max_length=50),
        ),
    ]
