from django.contrib.auth import get_user_model
from django.db import models

from notes.validators import validate_parus_url

NULLABLE = {
    "blank": True,
    "null": True,
}

User = get_user_model()


class UserProfile(models.Model):
    """Модель для профиля пользователя"""

    HUB_LEADER_PERMISSION_NAME = "ХАБ Лидер"

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    car_loan_center = models.ForeignKey(
        "CarLoanCenter",
        on_delete=models.CASCADE,
        verbose_name="Центр автокредитования",
        help_text="Выберите центр автокредитования",
    )

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


class Notes(models.Model):
    """Модель для записок"""

    class StatusNotes(models.TextChoices):
        DRAFT = "DRAFT", "Черновик"
        ACTIVE = "ACTIVE", "Активна"
        IN_PROGRESS = "IN_PROGRESS", "Действующая"

    pyrus_url = models.CharField(
        validators=[validate_parus_url],
        max_length=255,
        verbose_name="Ссылка на Pyrus",
        help_text="Введите ссылку на Pyrus",
        **NULLABLE,
    )
    car_loan_center = models.ForeignKey(
        "CarLoanCenter",
        on_delete=models.CASCADE,
        verbose_name="Центр автокредитования",
        help_text="Выберите центр автокредитования",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата создания записки",
    )
    update_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
        help_text="Дата обновления записки",
    )
    appoval_date = models.DateTimeField(
        verbose_name="Дата утверждения",
        help_text="Дата утверждения записки",
        **NULLABLE,
    )
    subject = models.CharField(
        max_length=255,
        verbose_name="Тема записки",
        help_text="Введите тему записки",
    )
    owner = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
        help_text="Выберите пользователя",
        null=True,
    )
    observers = models.ManyToManyField(
        UserProfile,
        related_name="observers",
        verbose_name="Наблюдатели",
        help_text="Выберите наблюдателей",
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=StatusNotes.choices,
        default=StatusNotes.DRAFT,
        verbose_name="Статус записки",
        help_text="Выберите статус записки",
    )

    def __str__(self):
        """Возвращает строковое представление объекта"""
        status_display = self.get_status_display()
        formatted_date = self.created_at.strftime("%d.%m.%Y")
        return f"Записка {self.subject} Статус: {status_display} Дата: {formatted_date}"

    class Meta:
        verbose_name = "Записка"
        verbose_name_plural = "Записки"
        ordering = ["-created_at"]


class CarLoanCenter(models.Model):
    """Модель для центра автокредитования"""

    name = models.CharField(
        max_length=255,
        verbose_name="Название центра автокредитования",
        help_text="Введите название центра",
    )
    hub = models.ForeignKey(
        "Hub",
        on_delete=models.CASCADE,
        verbose_name="Хаб",
        help_text="Выберите хаб",
    )

    def __str__(self):
        """Возвращает строковое представление объекта"""
        return self.name

    class Meta:
        verbose_name = "Центр автокредитования"
        verbose_name_plural = "Центры автокредитования"
        ordering = ["name"]


class Hub(models.Model):
    """Модель для хаба"""

    name = models.CharField(
        max_length=255,
        verbose_name="Название хаба",
        help_text="Введите название хаба",
    )

    def __str__(self):
        """Возвращает строковое представление объекта"""
        return self.name

    class Meta:
        verbose_name = "Хаб"
        verbose_name_plural = "Хабы"
        ordering = ["name"]
