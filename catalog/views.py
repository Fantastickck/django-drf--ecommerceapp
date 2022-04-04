from django.http import HttpResponse
from django.shortcuts import render

from .models import Category, Product, Brand, Product_Feature


def get_categories(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'catalog/categories.html', context)


def get_category(request, slug):
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category__slug=slug)
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'catalog/category.html', context)


def get_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    brand = Brand.objects.get(product__id=product_id)
    features = Product_Feature.objects.filter(product__id=product_id)
    context = {
        'product': product,
        'brand': brand,
        'features': features,
    }
    return render(request, 'catalog/product.html', context)


def get_brands(request):
    brands = Brand.objects.all()
    context = {
        'brands': brands
    }
    return render(request, 'catalog/brands.html', context)


def get_brand(request, slug):
    brand = Brand.objects.get(slug=slug)
    categories = Category.objects.filter(brand__slug=slug)
    products = Product.objects.filter(brand__slug=slug)
    context = {
        'brand': brand,
        'categories': categories,
        'products': products,
    }
    return render(request, 'catalog/brand.html', context)