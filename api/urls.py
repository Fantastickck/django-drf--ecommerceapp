from django.urls import include, path, re_path

from .views import ListProductsView, ProductDetailView, CategoryListView, ProductsByCategoryListView, \
    ProfileDetailView, FavouritesDatailView, FavouritesItemCreateView, FavouritesItemDeleteView

urlpatterns = [
    path('catalog/categories/', CategoryListView.as_view()),
    path('catalog/categories/<slug:slug>/', ProductsByCategoryListView.as_view()),
    path('catalog/products/', ListProductsView.as_view()),
    path('catalog/products/<int:pk>/', ProductDetailView.as_view()),
    path('profiles/<slug:slug>/', ProfileDetailView.as_view()),
    path('favourites/', FavouritesItemCreateView.as_view()),
    path('favourites/delete/<int:pk>', FavouritesItemDeleteView.as_view()),
    path('favourites/<slug:slug>/', FavouritesDatailView.as_view()),
    # path('auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('authenticate/', include('djoser.urls.authtoken')),
    # path('user/', UserDetailView.as_view())
    # path('products/<int:id>', DetailProductView.as_view())
]
