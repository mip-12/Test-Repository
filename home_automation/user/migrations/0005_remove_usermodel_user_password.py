# Generated by Django 3.1.5 on 2022-10-06 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20221006_0517'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermodel',
            name='user_password',
        ),
    ]
