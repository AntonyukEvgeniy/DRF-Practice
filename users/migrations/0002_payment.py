# Generated by Django 5.1.7 on 2025-03-30 20:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lms", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
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
                    "payment_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты"),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Сумма оплаты"
                    ),
                ),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("cash", "Наличные"),
                            ("transfer", "Перевод на счет"),
                            ("card", "Оплата картой"),
                        ],
                        default="card",
                        max_length=50,
                        verbose_name="Способ оплаты",
                    ),
                ),
                (
                    "paid_course",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to="lms.course",
                        verbose_name="Оплаченный курс",
                    ),
                ),
                (
                    "paid_lesson",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to="lms.lesson",
                        verbose_name="Оплаченный урок",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Платеж",
                "verbose_name_plural": "Платежи",
                "ordering": ["-payment_date"],
            },
        ),
    ]
