from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Product Name')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Product Description')
    category = models.ForeignKey('webapp.Category', related_name='product_category', on_delete=models.PROTECT,verbose_name='Product Category', null=False, blank=False)
    picture = models.ImageField(null=True, blank=True, upload_to='product_pics', default = 'default.jpg' ,verbose_name='Product Image')


    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return "{}. {}".format(self.pk, self.name)


class Category(models.Model):
    category = models.CharField(max_length=15, null=False, blank=False, verbose_name='Category')

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category

class Review(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name='tasks'
    )
    product = models.ForeignKey('webapp.Product', related_name='review', on_delete=models.CASCADE, verbose_name='Product', null=False, blank=False)
    review = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Review Description')
    rating = models.IntegerField(validators=(MinValueValidator(0),MaxValueValidator(5)), verbose_name='Rating')
    is_moderated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reviews'
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return "{}. {}: {}".format(self.pk, self.author, self.rating)
