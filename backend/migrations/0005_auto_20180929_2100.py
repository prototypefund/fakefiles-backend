# Generated by Django 2.1.1 on 2018-09-29 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20180929_2053'),
    ]

    operations = [
        migrations.RenameField(
            model_name='factcheck',
            old_name='pup_date_show_day',
            new_name='pub_date_show_day',
        ),
        migrations.RenameField(
            model_name='factcheck',
            old_name='pup_date_show_month',
            new_name='pub_date_show_month',
        ),
        migrations.RenameField(
            model_name='factcheck',
            old_name='pup_date_show_time',
            new_name='pub_date_show_time',
        ),
        migrations.RenameField(
            model_name='occurence',
            old_name='pup_date_show_day',
            new_name='pub_date_show_day',
        ),
        migrations.RenameField(
            model_name='occurence',
            old_name='pup_date_show_month',
            new_name='pub_date_show_month',
        ),
        migrations.RenameField(
            model_name='occurence',
            old_name='pup_date_show_time',
            new_name='pub_date_show_time',
        ),
    ]
