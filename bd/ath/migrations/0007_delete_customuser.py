# Generated by Django 5.0.1 on 2024-03-05 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ath', '0006_customuser_delete_userprofile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]