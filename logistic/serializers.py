from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):
    #serializer for product item in stock
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

    def validate_positions(self,value):
        if not value:
            raise serializers.ValidationError('Product items not listed')
        product_ids = [item['product'].id for item in value]
        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError('You can not duplicate items in the order')
        for item in value:
            if item['quantity'] == 0:
                raise serializers.ValidationError('Quantity of goods can only be a positive number')

        return value


    def create(self, validated_data):

        positions = validated_data.pop('positions')
        stock = Stock.objects.create(**validated_data)
        for object in positions:
            StockProduct.objects.create(stock=stock, **object)
        return stock


    def update(self, instance, validated_data):

        positions= validated_data.pop('positions')
        remove_items = {item.id: item for item in instance.positions.all()}

        for item in positions:
            item_id = item.get('id', None)
            if item_id is None:
                instance.positions.create(**item)
            elif remove_items.get(item_id, None) is not None:
                instance_item = remove_items.pop(item_id)
                Stock.objects.filter(id=instance_item.id).update(**item)

        for item in remove_items.values():
            item.delete()

        for field in validated_data:
            setattr(instance, field, validated_data.get(field, getattr(instance, field)))
        instance.save()

        return instance








