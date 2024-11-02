# Generated by Django 4.2.16 on 2024-11-01 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cars", "0003_carreservation_preco_total"),
    ]

    operations = [
        migrations.AlterField(
            model_name="carreservation",
            name="status",
            field=models.CharField(
                choices=[
                    ("EM_BREVE", "Em Breve"),
                    ("CONCLUIDA", "Concluída"),
                    ("CANCELADA", "Cancelada"),
                ],
                default="EM_BREVE",
                max_length=20,
            ),
        ),
    ]