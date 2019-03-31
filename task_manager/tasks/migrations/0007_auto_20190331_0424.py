# Generated by Django 2.1.5 on 2019-03-30 22:54

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0006_auto_20190331_0418'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taskassignees',
            old_name='assignee',
            new_name='user',
        ),
        migrations.AlterUniqueTogether(
            name='taskassignees',
            unique_together={('task', 'user')},
        ),
    ]