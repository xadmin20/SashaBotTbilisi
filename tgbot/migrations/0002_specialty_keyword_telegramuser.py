# Generated by Django 5.1.3 on 2024-11-13 14:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tgbot", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Specialty",
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
                (
                    "name",
                    models.CharField(
                        help_text="Название специальности (например, 'Электрик')",
                        max_length=100,
                        unique=True,
                        verbose_name="Название специальности",
                    ),
                ),
            ],
            options={
                "verbose_name": "Специальность",
                "verbose_name_plural": "Специальности",
            },
        ),
        migrations.CreateModel(
            name="Keyword",
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
                (
                    "word",
                    models.CharField(
                        help_text="Ключевое слово или фраза для обнаружения (например, 'лампочка')",
                        max_length=100,
                        verbose_name="Ключевое слово",
                    ),
                ),
                (
                    "specialty",
                    models.ForeignKey(
                        help_text="Специальность, к которой относится ключевое слово",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="keywords",
                        to="tgbot.specialty",
                        verbose_name="Специальность",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ключевое слово",
                "verbose_name_plural": "Ключевые слова",
            },
        ),
        migrations.CreateModel(
            name="TelegramUser",
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
                (
                    "telegram_id",
                    models.BigIntegerField(
                        help_text="ID пользователя Телеграм",
                        verbose_name="ID пользователя",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        blank=True,
                        help_text="Имя пользователя Телеграм",
                        max_length=255,
                        null=True,
                        verbose_name="Имя пользователя",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        help_text="Имя пользователя Телеграм",
                        max_length=255,
                        verbose_name="Имя",
                    ),
                ),
                (
                    "is_bot",
                    models.BooleanField(
                        default=False, help_text="Признак бота", verbose_name="Бот"
                    ),
                ),
                (
                    "specialties",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Специальности пользователя",
                        related_name="users",
                        to="tgbot.specialty",
                        verbose_name="Специальности",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пользователь Телеграм",
                "verbose_name_plural": "Пользователи Телеграм",
            },
        ),
    ]
