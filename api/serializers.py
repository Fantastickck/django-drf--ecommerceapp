from rest_framework import serializers

from catalog.models import Category, Product, Feature, ProductFeature
from main.models import AdvUser, Profile
from user_product.models import Favourites, FavouritesItem, Feedback


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'


class ProductSerializerForFavourites(serializers.ModelSerializer):
    category = serializers.CharField()
    brand = serializers.CharField()

    class Meta:
        model = Product
        fields = '__all__'


class FavouritesItemSerializer(serializers.ModelSerializer):
    product = ProductSerializerForFavourites(many=False)

    class Meta:
        model = FavouritesItem
        exclude = ['id', 'favourites']


class FavouritesSerializer(serializers.ModelSerializer):
    items = FavouritesItemSerializer(many=True)
    user = serializers.CharField()
    total = serializers.SerializerMethodField(source='get_total')

    def get_total(self, favourites):
        return favourites.items.all().count()

    class Meta:
        model = Favourites
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=True)

    class Meta:
        model = AdvUser
        fields = '__all__'


class FeatureSerializer(serializers.ModelSerializer):
    feature = serializers.CharField()

    class Meta:
        model = ProductFeature
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    '''Сериалайзер для списка товаров'''

    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    '''Сериализатор для одного товара'''
    feedbacks = FeedbackSerializer(many=True)
    features = FeatureSerializer(many=True)
    total_feedbacks = serializers.SerializerMethodField(
        source='get_total_feedbacks')
    images = serializers.StringRelatedField(many=True)

    def get_total_feedbacks(self, product):
        return product.feedbacks.all().count()

    class Meta:
        model = Product
        fields = '__all__'


class CategoryListSerializer(serializers.ModelSerializer):
    '''Сериализатор для списка категорий'''
    class Meta:
        model = Category
        fields = '__all__'


class CategoryDetailSerializer(serializers.ModelSerializer):
    '''Сериализатор для одной категории'''
    products = ProductListSerializer(many=True)
    total = serializers.SerializerMethodField(source='get_total')

    def get_total(self, category):
        return category.products.all().count()

    class Meta:
        model = Category
        fields = ['name', 'slug', 'info', 'products', 'total']

