from django.urls import path

from .views import AddFavouritesItem, RemoveFeedback, order_create, GetOrdersByUser, CreateFeedback, GetFavourites, RemoveFavouritesItem

urlpatterns = [
    path('create-order/', order_create, name='order_create'),
    path('user/orders/<slug:slug>', GetOrdersByUser.as_view(), name='get_orders'),
    path('create-feedback/<int:product_id>/',
         CreateFeedback.as_view(), name='create_feedback'),
    path('delete_feedback/<int:feedback_id>/',
         RemoveFeedback.as_view(), name='remove_feedback'),
    path('favourites/', GetFavourites.as_view(), name='get_favourites'),
    path('favourites/add/<int:product_id>/',
         AddFavouritesItem.as_view(), name='add_favourites_item'),
    path('favourites/remove/<int:item_id>',
         RemoveFavouritesItem.as_view(), name='remove_favourite_item')
]
