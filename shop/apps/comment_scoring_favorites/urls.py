from django.urls import path
from . import views

app_name = 'csf'

urlpatterns = [
    path("create_comment/<slug:slug>/",views.CommentView.as_view(),name="create_comment"),
    path("add_score/",views.add_score,name="add_score"),
    path("add_to_favorites/",views.add_to_favorites,name="add_to_favorites"),
    path("user_favorites/",views.UserFavoriteView.as_view(),name="user_favorites"),
    path("status_of_favorite/",views.status_of_favorite,name="status_of_favorite"),
]