# Generated by Django 4.2.1 on 2023-06-09 04:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('familytree', '0016_persondocument'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='persondocument',
            options={'verbose_name': 'document'},
        ),
        migrations.AlterModelOptions(
            name='personmedia',
            options={'verbose_name': 'media', 'verbose_name_plural': 'media'},
        ),
        migrations.AlterField(
            model_name='persondocument',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentation', to='familytree.person'),
        ),
    ]