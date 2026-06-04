from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.PROTECT)
    weight = models.CharField(max_length=50, default="1kg")
    weights = models.JSONField(default=list, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.8)
    reviews = models.PositiveIntegerField(default=0)
    image = models.URLField(max_length=1000, blank=True)
    images = models.JSONField(default=list, blank=True)
    is_featured = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    tag = models.CharField(max_length=80, blank=True)

    class Meta:
        ordering = ["category__name", "name"]

    def __str__(self):
        return self.name


class GalleryItem(TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=120, default="Factory")
    image = models.URLField(max_length=1000)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Testimonial(TimeStampedModel):
    name = models.CharField(max_length=180)
    role = models.CharField(max_length=180, blank=True)
    location = models.CharField(max_length=180, blank=True)
    quote = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Enquiry(TimeStampedModel):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Contacted", "Contacted"),
        ("Closed", "Closed"),
    ]

    name = models.CharField(max_length=180)
    business = models.CharField(max_length=255, blank=True, default="Retail Customer")
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=120, blank=True)
    message = models.TextField(blank=True)
    type = models.CharField(max_length=80, default="Inquiry")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Pending")

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Enquiries"

    def __str__(self):
        return f"{self.name} - {self.status}"


class Order(TimeStampedModel):
    STATUS_CHOICES = [
        ("Awaiting Shipment", "Awaiting Shipment"),
        ("Packed", "Packed"),
        ("Out for Delivery", "Out for Delivery"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]

    order_id = models.CharField(max_length=40, unique=True)
    customer_name = models.CharField(max_length=180, blank=True)
    customer_phone = models.CharField(max_length=30, blank=True)
    customer_email = models.EmailField(blank=True)
    shipping_address = models.TextField(blank=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    gst = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default="Awaiting Shipment")
    timeline = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.order_id


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    product_name = models.CharField(max_length=255)
    chosen_weight = models.CharField(max_length=50, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def line_total(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"


class SiteSettings(TimeStampedModel):
    brand_name = models.CharField(max_length=120, default="Impal Food")
    tagline = models.CharField(max_length=255, default="Purity. Trust. Quality.")
    hero_description = models.TextField(blank=True)
    about_heading = models.CharField(max_length=255, blank=True)
    about_p1 = models.TextField(blank=True)
    about_p2 = models.TextField(blank=True)
    about_p3 = models.TextField(blank=True)
    hero_image = models.URLField(max_length=1000, blank=True)
    whatsapp_number = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    facebook_url = models.URLField(max_length=500, blank=True)
    instagram_url = models.URLField(max_length=500, blank=True)
    linkedin_url = models.URLField(max_length=500, blank=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_desc = models.TextField(blank=True)
    meta_keywords = models.TextField(blank=True)
    ecommerce_active = models.BooleanField(default=True)
    display_public_prices = models.BooleanField(default=True)
    google_maps_embed = models.TextField(blank=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.brand_name
