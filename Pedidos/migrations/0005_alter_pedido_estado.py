# Generated by Django 5.0.6 on 2024-10-16 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0004_alter_pedido_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='estado',
            field=models.CharField(choices=[('P', 'Pendiente'), ('E', 'Enviado'), ('F', 'Entregado'), ('C', 'Cancelado')], default='P', max_length=1),
        ),
    ]
