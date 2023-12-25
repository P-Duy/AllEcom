from django.db.models import Min, Max

from core.models import (
    Product,
    ProductImages,
    Category,
    Vendor,
    Tags,
    ProductReview,
    CartOrder,
    CartOrderItems,
    wishlist,
    Address,
)


def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))
    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
    vendors = Vendor.objects.all()
    context = {
        "address": address,
        "categories": categories,
        "vendors": vendors,
        "min_max_price": min_max_price,
    }
    return context
