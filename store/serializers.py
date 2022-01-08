from decimal import Decimal
from django.core import validators
from rest_framework import serializers
from .models import Product, Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'price_with_tax', 'collection']

    price = serializers.DecimalField(
        max_digits=8, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')
    collection = CollectionSerializer()

    def calculate_tax(self, product: Product):
        return round(product.unit_price * Decimal(1.1), 2)

    def validate(self, data):
        if data['price'] < 1:
            return serializers.ValidationError("Price should be greater than 1")
        return data

    # Overwrite create method of serialier
    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return product

    # def update(self, instance, validated_data):
    #     instance.price = validated_data['price']
    #     instance.save()
    #     return instance
