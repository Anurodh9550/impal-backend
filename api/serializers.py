from rest_framework import serializers

from .models import (
    Category,
    Enquiry,
    GalleryItem,
    Order,
    OrderItem,
    Product,
    SiteSettings,
    Testimonial,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class GalleryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryItem
        fields = "__all__"


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = "__all__"


class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = "__all__"
        read_only_fields = ("status",)


class AdminEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    line_total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product",
            "product_name",
            "chosen_weight",
            "quantity",
            "unit_price",
            "line_total",
        )


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("order_id", "gst", "total", "timeline")

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        subtotal = sum(item["unit_price"] * item["quantity"] for item in items_data)
        gst = round(subtotal * 0.05, 2)
        order = Order.objects.create(
            **validated_data,
            subtotal=subtotal,
            gst=gst,
            total=subtotal + gst,
            timeline=["Order Placed", "Awaiting Shipment"],
        )
        order.order_id = f"IMP-{order.id:06d}"
        order.save(update_fields=["order_id"])
        for item in items_data:
            product = item.get("product")
            if product and product.stock >= item["quantity"]:
                product.stock -= item["quantity"]
                product.save(update_fields=["stock"])
            OrderItem.objects.create(order=order, **item)
        return order


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = "__all__"
