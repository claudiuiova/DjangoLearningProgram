# Generated by Django 2.0 on 2018-04-26 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20180424_1351'),
    ]

    operations = [
        migrations.RenameField(
            model_name='page',
            old_name='page',
            new_name='poll',
        ),
    ]