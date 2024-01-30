from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=128)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    pr_name = models.CharField(max_length=512)
    pr_count = models.IntegerField()
    pr_des = models.TextField(blank=True)
    pr_photo = models.ImageField(upload_to='media')
    pr_price = models.FloatField()
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    added_data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pr_name


class Cart(models.Model):
    user_id = models.IntegerField()
    user_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_product_quantity = models.IntegerField()
    user_added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_product
