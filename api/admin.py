from django.contrib import admin

from .models import Category, Enquiry, GalleryItem, Order, OrderItem, Product, SiteSettings, Testimonial


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    list_filter = ("is_active",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "is_featured", "is_visible")
    list_filter = ("category", "is_featured", "is_visible")
    search_fields = ("name", "description", "tag")


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_visible", "created_at")
    list_filter = ("category", "is_visible")
    search_fields = ("title", "description")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "location", "rating", "is_visible")
    list_filter = ("rating", "is_visible")
    search_fields = ("name", "role", "location", "quote")


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "type", "status", "created_at")
    list_filter = ("type", "status")
    search_fields = ("name", "business", "phone", "email", "city", "state")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "customer_name", "status", "subtotal", "gst", "total", "created_at")
    list_filter = ("status",)
    search_fields = ("order_id", "customer_name", "customer_phone", "customer_email")
    inlines = [OrderItemInline]


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("brand_name", "tagline", "email", "phone", "updated_at")
