# Generated by Django 5.0.7 on 2024-09-15 23:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Pessoas', '0004_pessoas_numemro'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pessoas',
            old_name='numemro',
            new_name='numero',
        ),
    ]
