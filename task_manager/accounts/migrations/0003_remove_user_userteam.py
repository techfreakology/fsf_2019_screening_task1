# Generated by Django 2.1.5 on 2019-03-26 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_userteam'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='userteam',
        ),
    ]