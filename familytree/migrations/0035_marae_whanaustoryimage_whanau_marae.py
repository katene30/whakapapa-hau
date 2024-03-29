# Generated by Django 4.2.1 on 2023-10-14 00:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('familytree', '0034_whanaustory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marae',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('physical_address', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('phone_number', models.CharField(blank=True, default='', max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
            options={
                'verbose_name_plural': 'Marae',
            },
        ),
        migrations.CreateModel(
            name='WhanauStoryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='')),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('alt_text', models.CharField(help_text='Provide alternative text for the image. Alt text is used by screen readers to describe the image for visually impaired users.', max_length=50)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('whanau_story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='whanau_story_images', to='familytree.whanaustory')),
            ],
        ),
        migrations.AddField(
            model_name='whanau',
            name='marae',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='familytree.marae'),
        ),
    ]
