from django.urls import path
from .views import *

app_name = 'search'

urlpatterns = [
    path('',SearchResultsView.as_view(),name="search_view"),
]