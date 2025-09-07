from django.urls import path
from .views import *

app_name="products"
urlpatterns = [
    path("cheapest_products/",get_cheapest_products,name="cheapest_products"),
    path("last_products/",get_last_products,name="last_products"),
    path('popular_products_group/',get_popular_product_groups,name="popular_products_group"),
    path("product_details/<slug:slug>/",ProductDetailView.as_view(),name="product_details"),
    path("related_product/<slug:slug>/",get_related_products,name="related_product"),
    path("product_groups/",ProductGroupsView.as_view(),name="product_groups"),
    path("product_of_group/<slug:slug>/",ProductsByGroupView.as_view(),name="product_of_group"),
    path("ajax_admin/",filter_value_for_feature,name='filter_value_for_feature'),
    path("product_groups_partial/",get_product_groups,name="product_groups_partial"),
    path('filtering_product_brands_partial/<slug:slug>',get_brands,name="filtering_product_brands_partial"),
    path('filtering_features_partial/<slug:slug>',get_features_for_filtre,name="filtering_features_partial"),
    path('compare_list/',ShowCompareListView.as_view(),name='compare_list'),
    path('compare_table/',compare_table,name='compare_table'),
    path('add_to_compare_list/',add_to_compare_list,name='add_to_compare_list'),
    path('delete_from_compare_list/',delete_from_compare_list,name='delete_from_compare_list'),
    path('status_of_compare_list/',status_of_compare_list,name='status_of_compare_list'),

]


