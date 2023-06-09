# Generated by Django 4.2.1 on 2023-06-09 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('familytree', '0014_remove_person_hapu_personhapu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personmedia',
            name='file',
        ),
        migrations.AddField(
            model_name='personmedia',
            name='image',
            field=models.ImageField(default='', upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='personmedia',
            name='alt_text',
            field=models.CharField(default='', help_text='Provide alternative text for the image. Alt text is used by screen readers to describe the image for visually impaired users.', max_length=50),
            preserve_default=False,
        ),
    ]
