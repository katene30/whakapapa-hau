# Generated by Django 4.2.1 on 2023-05-17 02:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('familytree', '0003_remove_person_children_alter_person_father_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='children',
            field=models.ManyToManyField(blank=True, related_name='related_children', to='familytree.person'),
        ),
        migrations.AlterField(
            model_name='person',
            name='father',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_father', to='familytree.person'),
        ),
        migrations.AlterField(
            model_name='person',
            name='mother',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_mother', to='familytree.person'),
        ),
    ]
