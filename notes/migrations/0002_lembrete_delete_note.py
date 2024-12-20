# Generated by Django 4.2.16 on 2024-10-31 11:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("notes", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Lembrete",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("titulo", models.CharField(max_length=255)),
                ("descricao", models.TextField()),
                ("data_criacao", models.DateTimeField(auto_now_add=True)),
                ("data_expiracao", models.DateField()),
                (
                    "categoria",
                    models.CharField(
                        choices=[
                            ("Reunião", "Reunião"),
                            ("Urgente", "Urgente"),
                            ("Notícia", "Notícia"),
                            ("Geral", "Geral"),
                            ("Tarefas Diárias", "Tarefas Diárias"),
                        ],
                        max_length=50,
                    ),
                ),
                ("status_ok", models.BooleanField(default=False)),
                (
                    "criador",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lembretes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-data_criacao"],
            },
        ),
        migrations.DeleteModel(
            name="Note",
        ),
    ]
