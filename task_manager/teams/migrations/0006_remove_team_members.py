# Generated by Django 2.1.5 on 2019-03-26 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0005_auto_20190326_1316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='members',
        ),
    ]
