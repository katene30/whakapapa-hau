# Generated by Django 4.2.1 on 2023-05-16 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('familytree', '0002_alter_person_options_remove_person_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='children',
        ),
        migrations.AlterField(
            model_name='person',
            name='father',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_father', to='familytree.person'),
        ),
        migrations.AlterField(
            model_name='person',
            name='mother',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_mother', to='familytree.person'),
        ),
        migrations.AlterField(
            model_name='person',
            name='siblings',
            field=models.ManyToManyField(blank=True, related_name='related_siblings', to='familytree.person'),
        ),
    ]
