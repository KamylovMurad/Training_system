# Generated by Django 4.2.1 on 2023-09-23 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training_site', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='duration_seconds',
            new_name='duration',
        ),
    ]
