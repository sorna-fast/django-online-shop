from django.urls import path
from . import views

app_name = "orders"
urlpatterns = [
    
    path('shop_cart/', views.ShopCartView.as_view(), name='shop_cart'),
    path("show_shop_cart/",views.show_shop_cart_View,name="show_shop_cart"),
    path("add_to_shop_cart/", views.add_to_shop_cart_view, name="add_to_shop_cart"),
    path("delete_from_shop_cart/",views.delete_from_shop_cart_View,name="delete_from_shop_cart"),
    path("update_shop_cart/",views.update_shop_cart,name="update_shop_cart"),
    path("status_of_shop_cart/",views.status_of_shop_cart,name="status_of_shop_cart"),
    path("create_order/",views.CreateOrderView.as_view(),name="create_order"),
    path("checkout_order/<int:order_id>/",views.CheckoutOrderViwe.as_view(),name="checkout_order"),
    path("applay_coupon/<int:order_id>/",views.ApplayCoupon.as_view(),name="applay_coupon"),
]