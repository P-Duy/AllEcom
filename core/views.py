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
    products = Product.objects.filter(product_status="published")

    context = {"products": products}
    return render(request, "core/index.html", context)
