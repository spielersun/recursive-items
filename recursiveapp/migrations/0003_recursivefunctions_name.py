# Generated by Django 2.1.1 on 2018-09-20 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recursiveapp', '0002_auto_20180920_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='recursivefunctions',
            name='name',
            field=models.CharField(default='name', max_length=50),
        ),
    ]
