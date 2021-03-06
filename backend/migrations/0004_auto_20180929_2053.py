# Generated by Django 2.1.1 on 2018-09-29 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20180929_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='factcheck',
            name='pup_date_show_day',
            field=models.BooleanField(default=True, verbose_name='Show day?'),
        ),
        migrations.AddField(
            model_name='factcheck',
            name='pup_date_show_month',
            field=models.BooleanField(default=True, verbose_name='Show month?'),
        ),
        migrations.AddField(
            model_name='factcheck',
            name='pup_date_show_time',
            field=models.BooleanField(default=True, verbose_name='Show time?'),
        ),
        migrations.AddField(
            model_name='occurence',
            name='pup_date_show_day',
            field=models.BooleanField(default=True, verbose_name='Show day?'),
        ),
        migrations.AddField(
            model_name='occurence',
            name='pup_date_show_month',
            field=models.BooleanField(default=True, verbose_name='Show month?'),
        ),
        migrations.AddField(
            model_name='occurence',
            name='pup_date_show_time',
            field=models.BooleanField(default=True, verbose_name='Show time?'),
        ),
        migrations.AlterField(
            model_name='factcheck',
            name='lang',
            field=models.ForeignKey(limit_choices_to={'category__translations__name': 'LANGUAGE'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.Tag', verbose_name='Language'),
        ),
        migrations.AlterField(
            model_name='occurence',
            name='lang',
            field=models.ForeignKey(limit_choices_to={'category__translations__name': 'LANGUAGE'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.Tag', verbose_name='Language'),
        ),
    ]
