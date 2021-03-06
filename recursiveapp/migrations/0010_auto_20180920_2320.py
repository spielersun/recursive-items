# Generated by Django 2.1.1 on 2018-09-20 20:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recursiveapp', '0009_auto_20180920_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recursivefunctions',
            name='name',
            field=models.CharField(default='name', max_length=50, unique=True, validators=[django.core.validators.RegexValidator('[A-Za-z0-9_]+', "Function name shouldn't contain ")]),
        ),
    ]
