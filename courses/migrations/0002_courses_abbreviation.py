# Generated by Django 3.1.1 on 2020-09-30 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='abbreviation',
            field=models.CharField(default='abc', max_length=6, unique=True),
        ),
    ]
