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
    queryset = FavouritesItem.objects.all()
    serializer_class = FavouritesItemSerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        user = AdvUser.objects.get(profile__slug=self.kwargs['slug'])
        queryset = FavouritesItem.objects.filter(favourites__user=user).prefetch_related('product').select_related('product')
        return queryset
    

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdvUser.objects.all()

    def get_queryset(self):
        pass


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all().prefetch_related('feedbacks').prefetch_related('features').prefetch_related('images')
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
