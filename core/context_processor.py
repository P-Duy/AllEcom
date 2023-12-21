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
    products = Product.objects.filter(product_status="published", featured=True)
    categories = Category.objects.all()
    context = {
        "products": products,
        "categories": categories,
    }
    return context
