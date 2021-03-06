from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование товара')
    description = models.TextField(blank=True, verbose_name='Описание товара')
    price = models.IntegerField(verbose_name='Цена товара')
    quantity = models.PositiveIntegerField(
        default=0, verbose_name='Количество товаров')
    quantity_of_purchases = models.PositiveIntegerField(
        default=0, verbose_name='Количество заказов товара')
    image = models.ImageField(
        upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Изображение товара')
    total_rating = models.DecimalField(
        max_digits=2, decimal_places=1, verbose_name='Общий рейтинг', null=True)
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, verbose_name='Категория', related_name='products')
    brand = models.ForeignKey(
        'Brand', on_delete=models.CASCADE, verbose_name='Бренд', related_name='products')

    def __str__(self):
        return self.name

    def get_total_rating(self):
        """Получение итогового рейтинга из отзывов."""
        count_feedback = self.feedbacks.count() if self.feedbacks.count() != 0 else 1
        sum_rating = sum(feedback.rating for feedback in self.feedbacks.all())
        return round(sum_rating/count_feedback, 1)

    def save(self, *args, **kwargs):
        self.total_rating = self.get_total_rating()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['price']


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images', verbose_name='Товар')
    image = models.ImageField(
        upload_to='products/%Y/%m/%d/', verbose_name='Изображения')

    def __str__(self):
        return str(self.image)


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Категория')
    info = models.TextField(blank=True, verbose_name='Описание категории')
    logo = models.ImageField(
        blank=True, upload_to='logos/%Y/%m/%d/', verbose_name='Лого Категории')

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
    logo = models.ImageField(
        blank=True, upload_to='logos/%Y/%m/%d/', verbose_name='Лого Бренда')
    category = models.ManyToManyField(
        Category, blank=True, related_name='brands')

    slug = models.SlugField(max_length=255, unique=True,
                            verbose_name='URL бренда')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class Feature(models.Model):
    """
    Модель наименования характеристики.
    """
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name='Категория')
    name = models.CharField(max_length=255, verbose_name='Особенность')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Особенность'
        verbose_name_plural = 'Особенности'


class ProductFeature(models.Model):
    """
    Модель значения характеристики.
    """
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='features')
    feature = models.ForeignKey(
        Feature, on_delete=models.PROTECT, related_name='features')
    value_float = models.DecimalField(
        blank=True, max_digits=10, decimal_places=1, verbose_name='Значение', null=True)
    value_text = models.TextField(
        blank=True, verbose_name='Значение', null=True)

    def __str__(self):
        return f'{self.feature.name} {self.value_float} {self.value_text}'

    class Meta:
        verbose_name = 'Характеристика товара'
        verbose_name_plural = 'Характеристики товаров'
