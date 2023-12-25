from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_list_or_404, get_object_or_404
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
from django.db.models import Count, Avg
from taggit.models import Tag
from core.forms import ProductReviewForm


# Create your views here.
def index(request):
    products = Product.objects.filter(product_status="published", featured=True)

    context = {
        "products": products,
    }
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


def vendor_list_view(request):
    vendors = Vendor.objects.all()

    context = {"vendors": vendors}
    return render(request, "core/vendor_list.html", context)


def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor, product_status="published")

    context = {
        "vendor": vendor,
        "products": products,
    }
    return render(request, "core/vendor_detail.html", context)


def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    p_images = product.p_images.all()
    products = Product.objects.filter(category=product.category).exclude(pid=pid)
    # Get product reviews
    product_reviews = ProductReview.objects.filter(product=product).order_by("-date")
    # Get product average rating

    avg_rating = ProductReview.objects.filter(product=product).aggregate(
        rating=Avg("rating")
    )
    # Product reviews form
    review_form = ProductReviewForm()

    make_review = True

    if request.user.is_authenticated:
        address = Address.objects.get(status=True, user=request.user)
        user_review_count = ProductReview.objects.filter(
            user=request.user, product=product
        ).count()

        if user_review_count > 0:
            make_review = False

    context = {
        "product": product,
        "reviews": product_reviews,
        "p_images": p_images,
        "products": products,
        "avg_rating": avg_rating,
        "review_form": review_form,
        "make_review": make_review,
    }
    return render(request, "core/product_detail.html", context)


def tag_list(request, tag_slug=None):
    tag = None
    products = Product.objects.filter(product_status="published").order_by("-id")
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
    else:
        products = Product.objects.all()
    context = {"tag": tag, "product": products}
    return render(request, "core/tag_list.html", context)


def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST["review"],
        rating=request.POST["rating"],
    )

    context = {
        "user": user.username,
        "review": request.POST["review"],
        "rating": request.POST["rating"],
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(
        rating=Avg("rating")
    )

    return JsonResponse(
        {
            "bool": True,
            "context": context,
            "average_reviews": average_reviews,
        }
    )
