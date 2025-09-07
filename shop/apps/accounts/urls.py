from django.urls import path
from .views import *

app_name="accounts"
urlpatterns = [
    path("register/",RegisterUserView.as_view(),name="register"),
    path("verify/",VerifyRegisterCodeView.as_view(),name="Verify"),
    path('login/',LoginUserView.as_view(),name="login"),
    path('logout/',LogoutUserView.as_view(),name="logout"),
    path('userpanel/',UserPanelView.as_view(),name="userpanel"),
    path('change_password/',ChangePasswordView.as_view(),name="change_password"),
    path('remember_password/',RemeberPasswordView.as_view(),name="remember_password"),
     path("show_last_orders/",show_last_orders,name="show_last_orders"),
    path("update_profile/",UpdateProfileView.as_view(),name="update_profile"),
    path("show_user_payments/",show_user_payments,name="show_user_payments"),
    path("return_to_shop_cart/<uuid:order_code>/",return_to_shop_cart,name="return_to_shop_cart"),
]
