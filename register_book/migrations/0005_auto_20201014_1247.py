# Generated by Django 3.1.1 on 2020-10-14 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0001_initial'),
        ('register_book', '0004_remove_registerbook_description'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='registerbook',
            unique_together={('subject', 'year')},
        ),
    ]
