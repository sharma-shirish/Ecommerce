from django.contrib import messages
from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, default="")
    image = models.ImageField(upload_to='static/shop/img/')

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Tags(models.Model):
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=500)
    Category = models.ForeignKey('Category', default="", on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = 'Tags'


class Products(models.Model):
    name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=500)
    price = models.FloatField(default=0.0)
    discount_price = models.FloatField(default=0.0)
    Category = models.ForeignKey('Category', default="", on_delete=models.DO_NOTHING)
    tags = models.ForeignKey('Tags', default="", on_delete=models.DO_NOTHING)
    count = models.IntegerField(default=0)
    image = models.ImageField(upload_to='static/shop/img/')
    image1 = models.ImageField(upload_to='static/shop/img/', null=True)
    image2 = models.ImageField(upload_to='static/shop/img/', null=True)
    image3 = models.ImageField(upload_to='static/shop/img/', null=True)
    image4 = models.ImageField(upload_to='static/shop/img/', null=True)

    @staticmethod
    def get_products_by_id(ids):
        return Products.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Products.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Products.objects.filter(Category=category_id)
        else:
            return Products.get_all_products()

    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return reverse("detail", kwargs={
            "pk": self.pk

        })

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            "pk": self.pk
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            "pk": self.pk
        })

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = 'Products'


class OrderItem(models.Model):
    customer = models.ForeignKey(User,
                                 on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

    # return the total price value of each product item
    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_items(self):
        return self.quantity

    # return the total price value of each product item based on discounted prices
    def get_discount_item_price(self):
        return self.quantity * self.item.discount_price

    # return the value of the price saved from existing discounts
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_discount_item_price()

    # return which function is used as a price determinant (whether using the original price or discounted price)
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    customer = models.ForeignKey(User,
                                 on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date_time = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateField(default=datetime.datetime.today)
    order_ordered = models.BooleanField(default=False)
    order_shipped = models.BooleanField(default=False)
    billing_address = models.CharField(max_length=50, default='', blank=True)
    shipping_address = models.CharField(max_length=50, default='', blank=True)
    shipping_phone = models.CharField(max_length=50, default='', blank=True)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-ordered_date')

    def __str__(self):
        return f"{self.customer}"

    # get_total_price, returns the value of the total price of all ordered product items
    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    # get_total_items_count, returns the total number of items of all ordered product items
    def get_total_items_count(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_items()
        return total

    def get_items_in_order(self):
        # items = self.items.all()
        return self.items.all()


class BillingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=5)

    def __str__(self):
        return self.user.name
