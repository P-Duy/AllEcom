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
    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
    vendors = Vendor.objects.all()
    context = {
        "address": address,
        "categories": categories,
        "vendors": vendors,
    }
    return context
