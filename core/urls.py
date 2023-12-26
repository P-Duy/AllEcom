from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Home page
    path("", views.index, name="index"),
    path("products/", views.product_list_view, name="product-list"),
    path("product/<pid>/", views.product_detail_view, name="product-detail"),
    # Category page
    path("categories/", views.category_list_view, name="categories-list"),
    path(
        "category/<cid>/",
        views.category_product_list_view,
        name="category-product-list",
    ),
    # Vendor page
    path("vendors/", views.vendor_list_view, name="vendors-list"),
    path("vendor/<vid>/", views.vendor_detail_view, name="vendor-detail"),
    # tags page
    path("products/tags/<slug:tag_slug>/", views.tag_list, name="tags"),
    # add related
    path("ajax-add-review/<int:pid>/", views.ajax_add_review, name="ajax-add-review"),
    # search
    path("search/", views.search_view, name="search"),
    # Filter product URL
    path("filter-products/", views.filter_product, name="filter-product"),
    # Add to cart URL
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    # Cart Page URL
    path("cart/", views.cart_view, name="cart"),
    # Delete ITem from Cart
    path("delete-from-cart/", views.delete_item_from_cart, name="delete-from-cart"),
    # Update  Cart
    path("update-cart/", views.update_cart, name="update-cart"),
]
