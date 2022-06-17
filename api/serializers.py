from functools import reduce

from rest_framework import serializers

from catalog.models import Category, Product, Feature, ProductFeature
from main.models import AdvUser, Profile
from user_product.models import Favourites, FavouritesItem, Feedback, Order, OrderItem


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'


class ProductSerializerForFavourites(serializers.ModelSerializer):
    """
    Сериализатор для товаров в избранном.
    """
    category = serializers.CharField()
    brand = serializers.CharField()

    class Meta:
        model = Product
        fields = '__all__'


class FavouritesItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavouritesItem
        fields = '__all__'


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


class FeedbackListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'user', 'product']


class FeedbackSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Feedback
        fields = '__all__'


class OrderItemDetailSerializer(serializers.ModelSerializer):
    """
    Детали элемента заказа.
    """
    product = serializers.CharField()

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    Детали одного заказа.
    """
    items = OrderItemDetailSerializer(many=True)
    total_price = serializers.SerializerMethodField(source='get_total_price')
    total_positions = serializers.SerializerMethodField(
        source='get_total_posititons')
    total_products = serializers.SerializerMethodField(
        source='get_total_products')

    def get_total_price(self, order):
        return order.get_total_cost()

    def get_total_positions(self, order):
        return order.items.count()

    def get_total_products(self, order):
        return reduce(lambda x, y: x + y, [item.quantity for item in order.items.all()])

    class Meta:
        model = Order
        fields = '__all__'


class OrderListSerializer(serializers.ModelSerializer):
    """
    Список заказов.
    """
    total_price = serializers.SerializerMethodField(source='get_total_price')

    def get_total_price(self, order):
        return order.get_total_cost()

    class Meta:
        model = Order
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка товаров.
    """
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для одного товара
    """
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
    """
    Сериализатор для списка категорий.
    """

    class Meta:
        model = Category
        fields = '__all__'


class CategoryDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для одной категории.
    """
    products = ProductListSerializer(many=True)
    total_products = serializers.SerializerMethodField(
        source='get_total_products')

    def get_total_products(self, category):
        return category.products.all().count()

    class Meta:
        model = Category
        fields = ['name', 'slug', 'info',  'total_products', 'products']
