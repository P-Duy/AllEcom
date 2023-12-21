from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Home page
    path("", views.index, name="index"),
    path("products/", views.product_list_view, name="product-list"),
    # Category page
    path("categories/", views.category_list_view, name="categories-list"),
    path(
        "category/<cid>/",
        views.category_product_list_view,
        name="category-product-list",
    ),
    # Vendor page
    path("vendors/", views.vendor_list_view, name="vendors-list"),
]
