# Generated by Django 3.2.6 on 2024-11-08 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autenticacao', '0006_rename_quantidade_estoque_estoque'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estoque',
            name='estoque',
        ),
        migrations.RemoveField(
            model_name='medicamento',
            name='quantidade',
        ),
        migrations.AddField(
            model_name='estoque',
            name='quantidade',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
