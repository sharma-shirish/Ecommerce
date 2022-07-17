from django.urls import include, path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('shop', views.shop, name='shop'),
    path('detail/<int:pk>', views.detail, name='detail'),
    path('add-to-cart/<pk>', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<pk>', views.remove_from_cart, name='remove-from-cart'),
    path('reduce-quantity-item/<pk>', views.reduce_quantity_item, name='reduce-quantity-item'),
    path('view-cart', views.view_cart, name='view_cart'),
    path('checkout', views.checkout, name='checkout'),
    path('test', views.test, name='test'),
]
