from django.db import models
from userProfile.models import Account
from product.models import Product


class CartItem(models.Model):
    user        =   models.ForeignKey(Account,on_delete=models.CASCADE, null=True)
    product     =   models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity    =   models.IntegerField(null=True)
    subtotal = models.FloatField(null = True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product.name
