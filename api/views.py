from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework import permissions

from catalog.models import Product, Category
from main.models import AdvUser, Profile
from user_product.models import Favourites, FavouritesItem, Feedback

from .permissions import IsAdminOrReadOnly, IsAuthorFeedback
from .serializers import CategoryListSerializer, CategoryDetailSerializer, FavouritesItemSerializer, FeedbackSerializer, ProductListSerializer, \
    ProductDetailSerializer, ProfileSerializer, FavouritesSerializer


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = ProfileSerializer
    lookup_field = 'slug'


class ProfileByUserView(generics.RetrieveUpdateDestroyAPIView):
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


class FeedbacksListView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class FeedbacksDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    permission_classes = [IsAuthorFeedback]
    serializer_class = FeedbackSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdvUser.objects.all()

    def get_queryset(self):
        pass


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all().prefetch_related(
        'feedbacks').prefetch_related('features').prefetch_related('features__feature').prefetch_related('images')
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProductDetailSerializer


class CategoryListView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Category.objects.all().order_by('pk')
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategoryListSerializer


class ProductsByCategoryListView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all().prefetch_related('products')
    serializer_class = CategoryDetailSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'


class ListProductsView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Product.objects.all().select_related('category').select_related('brand')
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProductListSerializer

    # def get_queryset(self):
    #     category = self.kwargs['slug']
    #     return Product.objects.filter(category=category)
