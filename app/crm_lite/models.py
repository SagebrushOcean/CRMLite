from django.db import models

class Company(models.Model):
    INN = models.CharField(
        verbose_name='ИНН',
        unique=True,
    )
    title = models.CharField(
        verbose_name='Название компании',
        max_length=255,
    )

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self):
        return f'Компания "{self.title}"'

class Storage(models.Model):
    address = models.CharField(
        verbose_name='Адрес',
    )
    company_id = models.ForeignKey(Company,
        on_delete=models.CASCADE,
        related_name='storage',
        verbose_name='Компания',
    )

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return f'Склад по адресу {self.address}'


# class Product(models.Model):
#     storage = models.PositiveIntegerField(
#         verbose_name="ID Склада"
#     )
#     title = models.CharField(
#         verbose_name="Наименование товара",
#         max_length=255,
#         null=False,
#         blank=False,
#     )
#     description = models.TextField(
#         verbose_name="Описание товара",
#         null=True,
#         blank=True
#     )
#     quantity = models.PositiveIntegerField(
#         verbose_name="Количество на складе",
#         default=0
#     )
#     purchase_price = models.DecimalField(
#         verbose_name="Закупочная стоимость",
#         max_digits=10,
#         decimal_places=2,
#         null=False,
#         blank=False,
#     )
#     sale_price = models.DecimalField(
#         verbose_namе="Цена продажи",
#         max_digits=10,
#         decimal_places=2,
#         null=False,
#         blank=False
#     )
#     created_at = models.DateTimeField(
#         verbose_name="Дата добавления",
#         auto_now_add=True
#     )
#     updated_at = models.DateTimeField(
#         verbose_name="Дата последнего обновления",
#         auto_now=True
#     )
#
#     class Meta:
#         verbose_name = "Товар"
#         verbose_name_plural = "Товары"
#         ordering = ["title"]
#
#     def __str__(self):
#         return f"{self.title} (Количество: {self.quantity})"
