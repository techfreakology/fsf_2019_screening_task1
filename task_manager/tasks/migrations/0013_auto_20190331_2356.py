# Generated by Django 2.1.1 on 2019-03-31 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0012_auto_20190331_2347'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together=set(),
        ),
    ]
