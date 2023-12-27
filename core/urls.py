from django.urls import path, include
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
    # Checkout  URL
    path("checkout/", views.checkout_view, name="checkout"),
    # Paypal URL
    path("paypal/", include("paypal.standard.ipn.urls")),
    # Payment Successful
    path("payment-completed/", views.payment_completed_view, name="payment-completed"),
    # Payment Failed
    path("payment-failed/", views.payment_failed_view, name="payment-failed"),
    # Dashboard URL
    path("dashboard/", views.customer_dashboard, name="dashboard"),
    # Order Detail URL
    path("dashboard/order/<int:id>", views.order_detail, name="order-detail"),
    # Making address defauly
    path(
        "make-default-address/", views.make_address_default, name="make-default-address"
    ),
    # wishlist page
    path("wishlist/", views.wishlist_view, name="wishlist"),
    # adding to wishlist
    path("add-to-wishlist/", views.add_to_wishlist, name="add-to-wishlist"),
]
