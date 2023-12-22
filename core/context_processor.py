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
    address = Address.objects.get(user=request.user)
    context = {
        "address": address,
        "categories": categories,
    }
    return context
