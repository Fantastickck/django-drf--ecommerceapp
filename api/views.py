from django.shortcuts import render
from rest_framework import viewsets, generics

from catalog.models import Product, Category
from main.models import AdvUser, Profile
from user_product.models import Favourites, FavouritesItem

from .serializers import CategoryListSerializer, CategoryDetailSerializer, FavouritesItemSerializer, ProductListSerializer, \
    ProductDetailSerializer, ProfileSerializer, FavouritesSerializer


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile
    serializer_class = ProfileSerializer
    lookup_field = 'slug'

    # def get_object(self):
    #     obj = Profile.objects.get(id=self.request.user.id)
    #     return obj


class FavouritesDatailView(generics.ListAPIView):
    queryset = Favourites.objects.all()
    serializer_class = FavouritesSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Favourites.objects.filter(user__profile__slug=self.kwargs['slug']).prefetch_related(
            'items', 'items__product', 'items__product__category', 'items__product__brand').select_related('user')
        return queryset


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdvUser.objects.all()

    def get_queryset(self):
        pass


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all().prefetch_related(
        'feedbacks').prefetch_related('features').prefetch_related('features__feature').prefetch_related('images')
    serializer_class = ProductDetailSerializer


class CategoryListView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Category.objects.all().order_by('pk')
    serializer_class = CategoryListSerializer


class ProductsByCategoryListView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all().prefetch_related('products')
    serializer_class = CategoryDetailSerializer
    lookup_field = 'slug'


class ListProductsView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    # def get_queryset(self):
    #     category = self.kwargs['slug']
    #     return Product.objects.filter(category=category)
