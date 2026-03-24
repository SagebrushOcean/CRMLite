from django.db import models
from django.utils import timezone

class Company(models.Model):
    INN = models.CharField(
        verbose_name='ИНН',
        unique=True,
        max_length=12
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
        max_length=255,
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


# class Supplier(models.Model):
#     company_id = models.ForeignKey(Company,
#         on_delete=models.CASCADE,
#         related_name='supplier',
#         verbose_name='Компания',
#     )
#     INN = models.CharField(
#         verbose_name='ИНН',
#         unique=True,
#         max_length=12
#     )
#     title = models.CharField(
#         verbose_name='Наименование поставщика',
#         max_length=255,
#     )
#
#     class Meta:
#         verbose_name = 'Поставщик'
#         verbose_name_plural = 'Поставщики'
#
#     def __str__(self):
#         return f'{self.title}'
#
# class Supply(models.Model):
#     supplier_id = models.ForeignKey(Supplier,
#         on_delete=models.CASCADE,
#         related_name='supplies',
#         verbose_name='Поставщик',
#     )
#     delivery_date = models.DateTimeField(
#         default=timezone.now,
#         verbose_name='Дата доставки',
#     )
#
#     class Meta:
#         verbose_name = 'Поставка'
#         verbose_name_plural = 'Поставки'
#
#     def __str__(self):
#         return f'Поставка {self.id}'
#
#
# class Product(models.Model):
#     storage_id = models.ForeignKey(Storage,
#         on_delete=models.CASCADE,
#         related_name='products',
#         verbose_name='Склад',
#     )
#     title = models.CharField(
#         verbose_name='Наименование товара',
#         max_length=255,
#     )
#     description = models.TextField(
#         verbose_name='Описание товара',
#         null=True,
#         blank=True
#     )
#     quantity = models.PositiveIntegerField(
#         verbose_name='Количество на складе',
#         default=0
#     )
#     purchase_price = models.DecimalField(
#         verbose_name='Закупочная стоимость',
#         max_digits=10,
#         decimal_places=2,
#     )
#     sale_price = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         verbose_name='Цена продажи',
#     )
#     created_at = models.DateTimeField(
#         verbose_name='Дата добавления',
#         auto_now_add=True
#     )
#     updated_at = models.DateTimeField(
#         verbose_name='Дата последнего обновления',
#         auto_now=True
#     )
#     supplies = models.ManyToManyField(Supply, through='SupplyProduct')
#
#     class Meta:
#         verbose_name = 'Товар'
#         verbose_name_plural = 'Товары'
#         ordering = ['title']
#
#     def __str__(self):
#         return f'{self.title} (Количество: {self.quantity})'
#
#
# class SupplyProduct(models.Model):
#     supply_id = models.ForeignKey(Supply,
#         on_delete=models.CASCADE,
#         verbose_name='ID поставки',
#     )
#     product_id = models.ForeignKey(Product,
#         on_delete=models.CASCADE,
#         verbose_name='Товар',
#     )
#     quantity = models.PositiveIntegerField(
#         verbose_name='Количество товара',
#     )
#
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['supply_id', 'product_id'], name='unique_product_supply'
#             )
#         ]
#
#     def __str__(self):
#         return f'{self.product_id.title} (поставка {self.supply_id.id})'
