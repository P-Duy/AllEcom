from django.urls import path
from core.views import index, product_list_view
from . import views

app_name = 'core'

urlpatterns = [
    path("", views.index, name="index"),
    path("products/", views.product_list_view, name="product-list"),
]
