from email.policy import default
from django.core.exceptions import ValidationError
from pyexpat import model
from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

STATUS_CHOICES = (
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)

RATING = (
    ("1", "★☆☆☆☆"),
    ("2", "★★☆☆☆"),
    ("3", "★★★☆☆"),
    ("4", "★★★★☆"),
    ("5", "★★★★★"),
)


def validate_file_extension(value):
    import os

    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = [".jpg", ".png", ".svg"]
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported file extension.")


# Create your models here.
def user_directory_path(instance, filename):
    return "user_{0}/{1}".format(instance.user.id, filename)


class Category(models.Model):
    cid = ShortUUIDField(
        unique=True, length=10, max_length=10, prefix="cat", alphabet="abcdefgh12"
    )
    title = models.CharField(max_length=100, default="Food")
    image = models.ImageField(
        upload_to="category",
        default="category.jpg",
    )
    svg = models.FileField(
        upload_to="category",
        default="category.jpg",
        validators=[validate_file_extension],
    )

    class Meta:
        verbose_name_plural = "categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def category_svg(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.svg.url))

    def __str__(self):
        return self.title


class Tags(models.Model):
    pass


class Vendor(models.Model):
    vid = ShortUUIDField(
        unique=True, length=10, max_length=10, prefix="ven", alphabet="abcdefgh12"
    )
    title = models.CharField(max_length=100, default="Duy")
    image = models.ImageField(upload_to=user_directory_path, default="user.jpg")
    cover_image = models.ImageField(upload_to=user_directory_path, default="user.jpg")
    description = RichTextUploadingField(blank=True, default="hello world")

    address = models.CharField(max_length=100, default="123 Hồ Chí Minh")
    contact = models.CharField(max_length=100, default="+123 (456) 789")
    chat_resp_time = models.CharField(max_length=100, default="100")
    shipping_on_time = models.CharField(max_length=100, default="100")
    authentic_rating = models.CharField(max_length=100, default="100")
    days_return = models.CharField(max_length=100, default="100")
    Warranty_period = models.CharField(max_length=100, default="100")
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = "Vendors"

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title


class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefgh12")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="category"
    )
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.SET_NULL,
        null=True,
        related_name="product",
    )

    title = models.CharField(max_length=100, default="Product Title")
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg")
    description = RichTextUploadingField(blank=True, default="this is the product")

    price = models.DecimalField(max_digits=9, decimal_places=2, default="2.22")  # 20.12
    old_price = models.DecimalField(max_digits=9, decimal_places=2, default="2.22")

    specifications = RichTextUploadingField(blank=True, default="this is the product")
    type = models.CharField(max_length=100, default="Organic", null=True, blank=True)
    stock_count = models.CharField(max_length=100, default="10", null=True, blank=True)
    life = models.CharField(max_length=100, default="100 ngày", null=True, blank=True)
    mdf = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    tags = TaggableManager(blank=True)

    product_status = models.CharField(
        choices=STATUS, max_length=10, default="in_review"
    )

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    sku = ShortUUIDField(
        unique=True,
        length=4,
        max_length=20,
        prefix="sku",
        alphabet="abcdefgh12",
    )

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

    def get_precentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price


class ProductImages(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="p_images",
        on_delete=models.SET_NULL,
        null=True,
    )
    image = models.ImageField(upload_to="product-images", default="product.jpg")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images"


#################### Cart, order, order item, and address####################


class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=3, default="2.22")  # 20.12
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(
        choices=STATUS, max_length=10, default="processing"
    )

    class Meta:
        verbose_name_plural = "Cart Order"


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=9, decimal_places=2, default="2.22")  # 20.12
    total = models.DecimalField(max_digits=10, decimal_places=2, default="22.22")

    class Meta:
        verbose_name_plural = "Cart Order Items"

    def order_image(self):
        return mark_safe(
            '<img src="/media/%s" width="50" height="50" />' % (self.image)
        )


#################### Product Review, wishlists, address ####################


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    rating = models.CharField(choices=RATING, default=None)
    review = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return self.product.title

    def get_rating(self):
        return self.rating


class wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlist"

    def __str__(self):
        return self.product.title


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"
