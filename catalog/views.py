import re

from django.views.generic import DetailView, ListView, View
from django.shortcuts import render, redirect

from .models import Category, Product, Brand, ProductFeature, Feature
from user_product.models import Feedback
from .filters import ProductFilter
from cart.forms import CartAddProductForm


class GetCategories(ListView):
    model = Category
    template_name = 'catalog/categories.html'
    context_object_name = 'categories'


class GetProducts(ListView):
    template_name = 'catalog/products.html'
    context_object_name = 'products'
    paginate_by = 5

    # Метод ля передачи передачи query параметров
    def get_query_string(self):
        query_string = self.request.META.get("QUERY_STRING", "")
        # Get all queries excluding pages from the request's meta
        validated_query_string = "&".join([x for x in re.findall(
            r"(\w*=\w{1,})", query_string) if not "page=" in x])
        # Avoid passing the query path to template if no search result is found using the previous query
        return "&" + validated_query_string.lower() if (validated_query_string) else ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(
            self.request.GET, queryset=self.get_queryset())
        # context['category'] = Category.objects.get(slug=self.kwargs['slug'])
        context['cart_product_form'] = CartAddProductForm()
        context['query_string'] = self.get_query_string()
        context['prev_url'] = self.request.META.get('HTTP_REFERER')
        return context

    # def get_queryset(self):
    #     if self.request.GET.get('brand'):
    #         return Product.objects.filter(category__slug=self.kwargs['slug'], brand__slug=self.request.GET.get('brand'))
    #     else:
    #         return Product.objects.filter(category__slug=self.kwargs['slug'])
    # def get_queryset(self):
    #     return Product.objects.filter(category__slug=self.kwargs['slug'])

    def get_queryset(self):
        # queryset = super().get_queryset()
        queryset = Product.objects.filter(category__slug=self.kwargs['slug'])
        return ProductFilter(self.request.GET, queryset=queryset).qs


class GetOneProduct(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    pk_url_kwarg = "product_id"

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['features'] = ProductFeature.objects.filter(
            product__id=self.kwargs['product_id']).select_related('feature')
        context['feedbacks'] = Feedback.objects.filter(product__id=self.kwargs['product_id']).select_related('user').prefetch_related('images')
        if self.request.user.is_authenticated:
            feedback_exist = Feedback.objects.filter(
                user=self.request.user, product=self.kwargs['product_id']).exists()
            context['feedback_exists'] = feedback_exist
        context['cart_product_form'] = CartAddProductForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class GetBrands(ListView):
    model = Brand
    template_name = 'catalog/brands.html'
    context_object_name = 'brands'


class GetCategoriesByBrand(ListView):
    template_name = 'catalog/categories_by_brand.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['products'] = Product.objects.filter(brand__slug=self.kwargs['slug'])
        context['products'] = Product.objects.filter(
            brand__id=self.kwargs['id'])
        # context['brand'] = Brand.objects.get(slug=self.kwargs['slug'])
        context['brand'] = Brand.objects.get(id=self.kwargs['id'])
        return context

    def get_queryset(self):
        return Category.objects.filter(brands__id=self.kwargs['id'])
