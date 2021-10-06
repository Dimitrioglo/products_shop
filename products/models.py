from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f'\nname: {self.name}\nprice: {self.price}\ndescription: {self.description}'


class ProductSpecifications(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="specification_product", blank=True)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=240)

    def __str__(self):
        return f'\nname:{self.product.name}\nkey:{self.key}\nvalue:{self.value}'
