# Generated by Django 2.1.5 on 2019-03-31 18:17

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0011_auto_20190331_1844'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together={('message', 'user'), ('task', 'message')},
        ),
    ]
