from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Product, Stock, StockProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductPositionSerializer(serializers.ModelSerializer):
    #сериализатор для позиции продукта на складе
    quantity = serializers.IntegerField(default=1)

    product = ProductSerializer()
    product = product['id']

    price = serializers.DecimalField(min_value=0, max_digits=18, decimal_places=2)

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    address = serializers.CharField()
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address','positions']
        depth = 1


    def create(self, validated_data):
        # address = serializers.CharField()
        # positions = ProductPositionSerializer(many=True)
        #
        # validated_data['address'] = address

        positions = validated_data.pop('positions')

        stock = super().create(validated_data)
        return stock

    def update(self, instance, validated_data):

        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        return stock
