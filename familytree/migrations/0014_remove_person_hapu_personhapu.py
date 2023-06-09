# Generated by Django 4.2.1 on 2023-06-07 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('familytree', '0013_alter_personmedia_options_remove_person_iwi_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='hapu',
        ),
        migrations.CreateModel(
            name='PersonHapu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hapu', models.CharField(blank=True, max_length=100, null=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hapu', to='familytree.person')),
            ],
            options={
                'verbose_name_plural': 'hapu',
            },
        ),
    ]
