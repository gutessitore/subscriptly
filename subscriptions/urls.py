from django.urls import path

from subscriptions import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload", views.upload_page, name="upload"),
    path("success", views.success_view, name="success"),
    path("home", views.home_view, name="home"),
    path("circle", views.circle_user_list_view, name="circle_user_list"),
    path("hotmart/extract", views.extract_hotmart_data, name="extract_hotmart_data"),
    path("hotmart", views.list_hotmart_users_view, name="list_hotmart_users"),
    path("compare", views.compare_users_view, name="compare_users"),
]