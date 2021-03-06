from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:list_id>", views.list_page, name="auctions_list"),
    path("comment/<int:list_id>", views.comment, name="comment"),
    path("create", views.create_listing, name="create_listing"),
    
]
