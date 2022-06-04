from decimal import Decimal

from django.db import models
from perfiles.models import Address, UserBase
from store.models import Articulo


class Order(models.Model):
    user = models.ForeignKey(
        UserBase, on_delete=models.CASCADE, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(
        Address, related_name='dir_facturacion', blank=True, null=True, on_delete=models.SET_NULL)
    shipping_address = models.ForeignKey(
        Address, related_name='dir_envio', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.reference_number

    @property
    def reference_number(self):
        return f"ORDER-{self.pk}"

    def get_raw_subtotal(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total

    def get_subtotal(self):
        subtotal = self.get_raw_subtotal() - self.get_impuesto()
        return subtotal

    def get_impuesto(self):
        valor_impuesto = 16
        impuesto = self.get_raw_subtotal() * valor_impuesto / 100
        return impuesto

    def get_raw_total(self):
        subtotal = self.get_raw_subtotal()
        # agregar suma de IGV, Delivery, Resta DESCUENTOS
        #total = subtotal - discounts + tax + delivery
        return subtotal

    def get_total(self):
        total = self.get_raw_total()
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

    def get_raw_total_item_price(self):
        if self.product.product.discount_price:
            precio_producto = self.product.product.discount_price
        else:
            precio_producto = self.product.product.store_price

        return self.quantity * precio_producto

    def get_total_item_price(self):
        price = self.get_raw_total_item_price()
        return price


class Payment(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.PROTECT, related_name='payments')
    payment_method = models.CharField(
        max_length=20, choices=(('Paypal', 'Paypal'),))
    timestamp = models.DateTimeField(auto_now_add=True)
    succesful = models.BooleanField(default=False)
    amount = models.FloatField()
    raw_response = models.TextField()

    def __str__(self):
        return self.reference_number

    @property
    def reference_number(self):
        return f"PAYMENT-{self.order}-{self.pk}"
