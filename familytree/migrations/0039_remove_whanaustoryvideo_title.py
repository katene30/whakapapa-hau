# Generated by Django 4.2.1 on 2023-10-15 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('familytree', '0038_remove_whanaustoryvideo_upload_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='whanaustoryvideo',
            name='title',
        ),
    ]
