
from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование товара')
    description = models.TextField(blank=True, verbose_name='Описание товара')
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Цена товара')
    count = models.IntegerField(default=0, verbose_name='Количество товаров')
    image = models.ImageField(blank=True, verbose_name='Изображение товара')
    category_id = models.ForeignKey(
        'Category', on_delete=models.CASCADE, verbose_name='Категория')
    brand_id = models.ForeignKey(
        'Brand', on_delete=models.CASCADE, verbose_name='Бренд')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Категория')
    info = models.TextField(blank=True, verbose_name='Описание категории')
    slug = models.SlugField(max_length=255, unique=True,
                            verbose_name='URL категории')

    def __str__(self): 
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Brand(models.Model):
    name = models.CharField(max_length=255, verbose_name='Бренд')
    info = models.TextField(blank=True, verbose_name='Описание бренда')

    categories = models.ManyToManyField(Category)

    slug = models.SlugField(max_length=255, verbose_name='URL бренда')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class Feature(models.Model):
    category_id = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name='Категория')
    name = models.CharField(max_length=255, verbose_name='Особенность')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Особенность'
        verbose_name_plural = 'Особенности'


class Product_Feature(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.PROTECT,)
    feature_id = models.ForeignKey(Feature, on_delete=models.PROTECT)
    value_float = models.DecimalField(
        blank=True, max_digits=10, decimal_places=1, verbose_name='Значение')
    value_text = models.TextField(blank=True, verbose_name='Значение')

    class Meta:
        verbose_name = 'Связь'
        verbose_name_plural = 'Связи'
