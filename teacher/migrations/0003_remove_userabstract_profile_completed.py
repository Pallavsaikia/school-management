# Generated by Django 3.1.1 on 2020-10-19 05:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_userabstract_profile_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userabstract',
            name='profile_completed',
        ),
    ]
