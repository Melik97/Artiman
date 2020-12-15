from rest_framework import serializers

from bot_service.models import Album, Product, Order, User


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['name', 'video', 'gif']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'id', 'image', 'stock')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('product', 'date', 'number')


class UserSerilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'order')

    pro = serializers.SerializerMethodField()

    def get_pro(self, instance):
        products_ = []
        p = instance.pro.get_queryset()
        for i in p:
            products_.append(i.pro)
        return products_
