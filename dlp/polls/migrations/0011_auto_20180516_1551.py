# Generated by Django 2.0 on 2018-05-16 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_poll_attempts'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='passed_poll',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='poll',
            name='attempts',
            field=models.IntegerField(),
        ),
    ]
