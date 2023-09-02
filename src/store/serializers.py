from rest_framework import serializers
from rest_framework.fields import DateTimeField

from src.store.models import Product, Category, ProductCategory


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)

    class Meta:
        model = Category
        fields = '__all__'


class ProductCreateSerializer(serializers.ModelSerializer):
    created = DateTimeField(read_only=True)
    title = serializers.CharField(max_length=256)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    is_published = serializers.BooleanField(default=True)
    is_deleted = serializers.BooleanField(default=False, read_only=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Product
        fields = ['id',
                  'created',
                  'title',
                  'price',
                  'is_published',
                  'is_deleted',
                  'categories']

    def create(self, validated_data):
        # print(validated_data)
        categories_data = validated_data.pop('categories')
        product = Product.objects.create(**validated_data)
        # print(product)
        for category_data in categories_data:
            category_name = category_data['name']
            existed_category = Category.objects.filter(name=category_name).first()
            if existed_category is not None:
                ProductCategory.objects.create(product=product,
                                               category=existed_category)
            else:
                new_category = Category.objects.create(name=category_name)
                ProductCategory.objects.create(product=product, category=new_category)
        return product


class ProductUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=256)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    is_published = serializers.BooleanField(default=True)
    is_deleted = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = ['id',
                  'title',
                  'price',
                  'is_published',
                  'is_deleted']

class ProductDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product


class ProductListSerializer(serializers.ModelSerializer):
    created = DateTimeField(read_only=True)
    title = serializers.CharField(max_length=256)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    is_published = serializers.BooleanField(default=True)
    is_deleted = serializers.BooleanField(default=False, read_only=True)
    categories = CategorySerializer(many=True)
    class Meta:
        model = Product
        fields = '__all__'
