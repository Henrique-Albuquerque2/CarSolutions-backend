# Generated by Django 4.2.16 on 2024-11-02 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cars", "0005_alter_carreservation_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="carreservation",
            name="status",
            field=models.CharField(
                choices=[
                    ("Em Breve", "Em Breve"),
                    ("Concluída", "Concluída"),
                    ("Cancelada", "Cancelada"),
                    ("Em Andamento", "Em Andamento"),
                ],
                default="EM_BREVE",
                max_length=20,
            ),
        ),
    ]
