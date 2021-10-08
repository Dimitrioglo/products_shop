from rest_framework import serializers
from .models import Product, ProductSpecifications
from drf_writable_nested import WritableNestedModelSerializer


class ProductSpecificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecifications
        fields = ['id', 'key', 'value', 'product']


class ProductSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    specification_product = ProductSpecificationsSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'user',
            'name',
            'price',
            'description',
            'specification_product'
        ]
        # read_only_fields = ('specification_product',)
