from django.db import models
from django.core.validators import MinValueValidator, \
    MaxValueValidator
from shop.models import Product
from account.models import Client


class Order(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField()
    address = models.CharField(max_length=150)
    postal_code = models.CharField(max_length=30)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    discount = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        total=sum(item.get_cost() for item in self.items.all()) 
        return (float(total)-self.discount)

    def get_discount(self, client):
        total = float(self.get_total_cost())
        if client.has_discount:
            if client.no_of_orders == 1:
                self.discount = total * 0.1
                print(self.discount)
                return self.discount
            elif client.no_of_orders > 3 and client.no_of_orders < 5:
                self.discount = total * 0.25
                print(self.discount)
                return self.discount
            else:
                self.discount = total * 0.40
                return self.discount
        else:
            return self.discount == 0

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
