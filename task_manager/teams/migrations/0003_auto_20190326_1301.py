# Generated by Django 2.1.5 on 2019-03-26 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_auto_20190326_1257'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='creator_by',
            new_name='creator',
        ),
    ]
