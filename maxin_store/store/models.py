import uuid

from django.db import models


# Create your models here.

class Products(models.Model):
    image = models.ImageField(upload_to='product_images/%Y/%m/%d/', max_length=255, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return self.name


class Size(models.Model):
    size = models.CharField(max_length=20)

    def __str__(self):
        return self.size


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    order_date = models.DateTimeField()

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    products = models.ManyToManyField(Products, blank=True)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return "Cart id: %s" % self.id
