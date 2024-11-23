from django.db import models

# Create your models here.


class TelegramBotToken(models.Model):
    """Токен бота Телеграм"""

    token = models.CharField(
        max_length=255, verbose_name="Токен бота", help_text="Токен бота из BotFather"
    )
    name = models.CharField(max_length=255, verbose_name="Название бота", default="Bot")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Токен бота"
        verbose_name_plural = "Токены ботов"


class TelegramUser(models.Model):
    """Пользователь Телеграм"""

    telegram_id = models.BigIntegerField(
        verbose_name="ID пользователя", help_text="ID пользователя Телеграм"
    )
    username = models.CharField(
        max_length=255, verbose_name="Имя пользователя", help_text="Имя пользователя Телеграм", null=True, blank=True
    )
    first_name = models.CharField(
        max_length=255, verbose_name="Имя", help_text="Имя пользователя Телеграм"
    )

    is_bot = models.BooleanField(
        default=False, verbose_name="Бот", help_text="Признак бота"
    )
    specialties = models.ManyToManyField(
        "Specialty",
        related_name="users",
        verbose_name="Специальности",
        help_text="Специальности пользователя",
        blank=True
    )

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = "Пользователь Телеграм"
        verbose_name_plural = "Пользователи Телеграм"


class Specialty(models.Model):
    """Специальность, на которую реагирует бот"""

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название специальности",
        help_text="Название специальности (например, 'Электрик')"
    )


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Специальность"
        verbose_name_plural = "Специальности"


class Keyword(models.Model):
    """Ключевое слово, связанное со специальностью"""

    word = models.CharField(
        max_length=100,
        verbose_name="Ключевое слово",
        help_text="Ключевое слово или фраза для обнаружения (например, 'лампочка')"
    )
    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.CASCADE,
        related_name='keywords',
        verbose_name="Специальность",
        help_text="Специальность, к которой относится ключевое слово"
    )

    def __str__(self):
        return f"{self.word} ({self.specialty.name})"

    class Meta:
        verbose_name = "Ключевое слово"
        verbose_name_plural = "Ключевые слова"
