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
    Wishlist,
    Address,
)


def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))

    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.filter(user=request.user)
        except:
            messages.warning(
                request, "You need to login before accessing your wishlist."
            )
            wishlist = 0
    else:
        wishlist = 0
    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
    vendors = Vendor.objects.all()
    context = {
        "address": address,
        "categories": categories,
        "wishlist": wishlist,
        "vendors": vendors,
        "min_max_price": min_max_price,
    }
    return context
