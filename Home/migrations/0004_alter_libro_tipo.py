# Generated by Django 5.0.6 on 2024-12-19 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0003_alter_libro_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='tipo',
            field=models.CharField(choices=[('Indefinido', 'I'), ('Libro Fisico', 'F'), ('Audio Libro', 'A'), ('Ebook', 'E')], default='Libro Fisico', max_length=15),
        ),
    ]
