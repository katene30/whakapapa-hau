# Generated by Django 4.2.1 on 2023-06-21 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('familytree', '0033_alter_whanauimage_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='WhanauStory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('narrative', models.TextField()),
                ('whanau', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='whanau_stories', to='familytree.whanau')),
            ],
            options={
                'verbose_name_plural': 'Whanau Stories',
            },
        ),
    ]
