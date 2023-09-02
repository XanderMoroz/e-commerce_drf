from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=256, unique=True, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='ProductCategory')
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    is_published = models.BooleanField()
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.title} {self.created}'


class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
