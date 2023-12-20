from django.shortcuts import render, HttpResponse
from core.models import (
    Category,
    Vendor,
    Tags,
    Product,
    CartOrder,
    CartOrderItems,
    ProductImages,
    ProductReview,
    wishlist,
    Address,
)

# Create your views here.
def index(request):
    products = Product.objects.filter(product_status="published", featured=True)

    context = {"products": products}
    return render(request, "core/index.html", context)


def product_list_view(request):
    products = Product.objects.filter(product_status="published")
    context = {"products": products}
    return render(request, "core/product_list.html", context)


def category_list_view(request):
    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, "core/category_list.html", context)


def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    product = Product.objects.filter(category=category, product_status="published")

    context = {
        "product": product,
        "category": category,
    }
    return render(request, "core/category_product_list.html", context)
