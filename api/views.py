from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend

from catalog.models import Product, Category
from main.models import AdvUser, Profile
from user_product.models import Favourites, FavouritesItem, Feedback, Order, OrderItem


from .permissions import IsAdminOrReadOnly, IsAuthorFeedback
from .serializers import CategoryListSerializer, CategoryDetailSerializer, FavouritesItemSerializer, FeedbackSerializer, OrderDetailSerializer, ProductListSerializer, \
    ProductDetailSerializer, ProfileSerializer, FavouritesSerializer, OrderListSerializer
from .filters import ProductFilter, ProductByCategoryFilter


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdvUser.objects.all()

    def get_queryset(self):
        pass


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Детали профиля, детали для админов"""

    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = ProfileSerializer
    lookup_field = 'slug'


class ProfileByUserView(generics.RetrieveUpdateDestroyAPIView):
    """Детали профиля по авторизированному пользователю"""

    queryset = Profile.objects.all()
    # permission_classes = [permissions.IsAuthsenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        obj = Profile.objects.get(user__id=self.request.user.id)
        return obj


class FavouritesItemCreateView(generics.CreateAPIView):
    queryset = FavouritesItem
    serializer_class = FavouritesItemSerializer


class FavouritesItemDeleteView(generics.DestroyAPIView):
    queryset = FavouritesItem
    serializer_class = FavouritesItemSerializer


class FavouritesDatailView(generics.ListAPIView):
    queryset = Favourites.objects.all()
    serializer_class = FavouritesSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Favourites.objects.filter(user__profile__slug=self.kwargs['slug']).prefetch_related(
            'items', 'items__product', 'items__product__category', 'items__product__brand').select_related('user')
        return queryset


class FeedbacksListView(generics.ListCreateAPIView):
    """Список отзывов"""
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class FeedbacksDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Детали одного отзыва. Полный доступ автору"""

    queryset = Feedback.objects.all()
    permission_classes = [IsAuthorFeedback]
    serializer_class = FeedbackSerializer


class OrdersByUserListView(generics.ListCreateAPIView):
    """Список заказов по пользователю"""

    queryset = Order.objects.all()
    serializer_class = OrderListSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(
            user__profile__slug=self.kwargs['slug']).prefetch_related('items')
        return queryset


class OrdersListView(generics.ListCreateAPIView):
    """Общий список заказов"""

    queryset = Order.objects.all().prefetch_related('items')
    serializer_class = OrderListSerializer


class OrdersDetailView(generics.RetrieveAPIView):
    """Детали одного заказа"""

    queryset = Order.objects.all().prefetch_related('items')
    serializer_class = OrderDetailSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Детали по одному продукту. Полный набор методов"""

    queryset = Product.objects.all().prefetch_related(
        'feedbacks', 'feedbacks__user', 'features', 'features__feature', 'images')
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProductDetailSerializer


class CategoryListView(generics.ListAPIView, generics.CreateAPIView):
    """Список категорий. Добавление категории"""

    queryset = Category.objects.all().order_by('pk')
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategoryListSerializer


class ProductsByCategoryListView(generics.RetrieveUpdateDestroyAPIView):
    """Список товаров по категории"""

    queryset = Category.objects.all().prefetch_related('products')
    serializer_class = CategoryDetailSerializer
    permission_classes = [IsAdminOrReadOnly]
    # filter_backends = (DjangoFilterBackend,)
    # filterset_class = ProductByCategoryFilter
    lookup_field = 'slug'


class ProductsListView(generics.ListAPIView, generics.CreateAPIView):
    """Общий список товаров. Добавление товара"""

    queryset = Product.objects.all().select_related('category', 'brand')
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProductListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     price = self.request.query_params.get('price').split('-')
    #     if len(price) == 2:
    #         queryset = queryset.filter(price__gte=int(price[0]), price__lte=int(price[1]))
    #     if len(price) == 1:
    #         queryset = queryset.filter(price=int(price[0]))
    #     return queryset
