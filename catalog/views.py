from django.views.generic import DetailView, ListView

from .filters import ProductFilter
from .models import Category, Product, Brand, ProductFeature
from user_product.models import Feedback
from cart.forms import CartAddProductForm


class GetCategories(ListView):
    """
    Представление списка 
    """
    model = Category
    template_name = 'catalog/categories.html'
    context_object_name = 'categories'


class GetProducts(ListView):
    """
    Представление списка продуктов одной категории.
    """
    template_name = 'catalog/products.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(
            self.request.GET, queryset=self.get_queryset())
        context['cart_product_form'] = CartAddProductForm()
        context['prev_url'] = self.request.META.get('HTTP_REFERER')
        return context

    def get_queryset(self):
        queryset = Product.objects.filter(category__slug=self.kwargs['slug'])
        return ProductFilter(self.request.GET, queryset=queryset).qs


class GetOneProduct(DetailView):
    """
    Представление информации об одном продукте.
    """
    model = Product
    template_name = 'catalog/product_detail.html'
    pk_url_kwarg = "product_id"

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['features'] = ProductFeature.objects.filter(
            product__id=self.kwargs['product_id']).select_related('feature')
        context['feedbacks'] = Feedback.objects.filter(
            product__id=self.kwargs['product_id']).select_related('user').prefetch_related('images')
        if self.request.user.is_authenticated:
            feedback_exist = Feedback.objects.filter(
                user=self.request.user, product=self.kwargs['product_id']).exists()
            context['feedback_exists'] = feedback_exist
        context['cart_product_form'] = CartAddProductForm()
        return context


class GetBrands(ListView):
    """
    Представление списка брендов.
    """
    model = Brand
    template_name = 'catalog/brands.html'
    context_object_name = 'brands'


class GetCategoriesByBrand(ListView):
    """
    Представление категорий у одного бренда.
    """
    template_name = 'catalog/categories_by_brand.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(
            brand__id=self.kwargs['id'])
        context['brand'] = Brand.objects.get(id=self.kwargs['id'])
        return context

    def get_queryset(self):
        return Category.objects.filter(brands__id=self.kwargs['id'])
