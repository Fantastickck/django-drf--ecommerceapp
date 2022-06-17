from django.urls import include, path, re_path

from .views import ProductsListView, ProductDetailView, CategoryListView, ProductsByCategoryListView, \
    ProfileDetailView, FavouritesDatailView, FavouritesItemCreateView, FavouritesItemDeleteView, ProfileByUserView, \
        FeedbacksListView, FeedbacksDetailView, OrdersByUserListView, OrdersListView, OrdersDetailView

from .yasg import urlpatterns as docs_urls

urlpatterns = [
    path('catalog/categories/', CategoryListView.as_view()),
    path('catalog/categories/<slug:slug>/', ProductsByCategoryListView.as_view()),
    path('catalog/products/', ProductsListView.as_view()),
    path('catalog/products/<int:pk>/', ProductDetailView.as_view()),
    path('profiles/me/', ProfileByUserView.as_view()),
    path('profiles/<slug:slug>/', ProfileDetailView.as_view()),
    path('profiles/<slug:slug>/orders/', OrdersByUserListView.as_view()),
    path('orders/', OrdersListView.as_view()),
    path('orders/<int:pk>', OrdersDetailView.as_view()),
    path('favourites/', FavouritesItemCreateView.as_view()),
    path('favourites/delete/<int:pk>', FavouritesItemDeleteView.as_view()),
    path('favourites/<slug:slug>/', FavouritesDatailView.as_view()),
    path('feedbacks/', FeedbacksListView.as_view()),
    path('feedbacks/<int:pk>/', FeedbacksDetailView.as_view()),
    path('auth/', include('djoser.urls')),
    path('authenticate/', include('djoser.urls.authtoken')),
]

urlpatterns += docs_urls
