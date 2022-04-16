from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from django.shortcuts import render

from .models import Category, Product, Brand, Product_Feature

from cart.forms import CartAddProductForm

class GetCategories(ListView):
    model = Category
    template_name = 'catalog/categories.html'
    context_object_name = 'categories'


class GetProducts(ListView):
    template_name = 'catalog/products.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs['slug'])
        context['cart_product_form'] = CartAddProductForm()
        return context

    def get_queryset(self):
        if self.request.GET.get('brand'):
            return Product.objects.filter(category__slug=self.kwargs['slug'], brand__slug=self.request.GET.get('brand'))
        else:
            return Product.objects.filter(category__slug=self.kwargs['slug'])


class GetOneProduct(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    pk_url_kwarg = "product_id"

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['features'] = Product_Feature.objects.filter(product__id=self.kwargs['product_id'])
        context['cart_product_form'] = CartAddProductForm()
        return context
        

class GetBrands(ListView):
    model = Brand
    template_name = 'catalog/brands.html'
    context_object_name = 'brands'


class GetCategoriesByBrand(ListView):
    template_name = 'catalog/categories_by_brand.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(brand__slug=self.kwargs['slug'])
        context['brand'] = Brand.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        return Category.objects.filter(brand__slug=self.kwargs['slug'])




# Контроллер для добавления товаров в корзину
# def product_detail(request, id):
#     product = get_object_or_404(Product, id=id, available=True)
#     cart_product_form = CartAddProductForm()
#     context = {
#         'product': product,
#         'cart_product_form': cart_product_form
#     }
#     return render(request, 'catalog/product_detail.html', context)