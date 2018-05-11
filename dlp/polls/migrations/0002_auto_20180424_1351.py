# Generated by Django 2.0 on 2018-04-24 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_index', models.CharField(max_length=200, verbose_name='Page index')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Poll', verbose_name='Poll')),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
        ),
        migrations.AlterField(
            model_name='question',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Page', verbose_name='Page'),
        ),
    ]