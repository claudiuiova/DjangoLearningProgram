# Generated by Django 2.0 on 2018-05-17 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0012_auto_20180517_1117'),
    ]

    operations = [
        migrations.CreateModel(
            name='PollStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stats', models.CharField(max_length=200, verbose_name='Poll Stats')),
            ],
        ),
    ]
