from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Enquiry, GalleryItem, Order, Product, SiteSettings, Testimonial
from .permissions import CreateOnlyOrAdmin, ReadOnlyOrAdmin
from .serializers import (
    AdminEnquirySerializer,
    CategorySerializer,
    EnquirySerializer,
    GalleryItemSerializer,
    OrderSerializer,
    ProductSerializer,
    SiteSettingsSerializer,
    TestimonialSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnlyOrAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    permission_classes = [ReadOnlyOrAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description", "category__name", "tag"]
    ordering_fields = ["name", "price", "stock", "created_at"]

    def get_queryset(self):
        qs = super().get_queryset()
        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(is_visible=True)
        category = self.request.query_params.get("category")
        if category and category.lower() != "all":
            qs = qs.filter(category__name__iexact=category)
        featured = self.request.query_params.get("featured")
        if featured in {"true", "1"}:
            qs = qs.filter(is_featured=True)
        return qs


class GalleryItemViewSet(viewsets.ModelViewSet):
    queryset = GalleryItem.objects.all()
    serializer_class = GalleryItemSerializer
    permission_classes = [ReadOnlyOrAdmin]

    def get_queryset(self):
        qs = super().get_queryset()
        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(is_visible=True)
        return qs


class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [ReadOnlyOrAdmin]

    def get_queryset(self):
        qs = super().get_queryset()
        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(is_visible=True)
        return qs


class EnquiryViewSet(viewsets.ModelViewSet):
    queryset = Enquiry.objects.all()
    permission_classes = [CreateOnlyOrAdmin]

    def get_serializer_class(self):
        if self.request.user and self.request.user.is_staff:
            return AdminEnquirySerializer
        return EnquirySerializer

    @action(detail=True, methods=["post"])
    def mark_contacted(self, request, pk=None):
        enquiry = self.get_object()
        enquiry.status = "Contacted"
        enquiry.save(update_fields=["status"])
        return Response(AdminEnquirySerializer(enquiry).data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items").all()
    serializer_class = OrderSerializer
    permission_classes = [CreateOnlyOrAdmin]

    @action(detail=True, methods=["post"])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get("status")
        valid_statuses = {choice[0] for choice in Order.STATUS_CHOICES}
        if new_status not in valid_statuses:
            return Response({"detail": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        order.status = new_status
        if new_status not in order.timeline:
            order.timeline.append(new_status)
        order.save(update_fields=["status", "timeline"])
        return Response(OrderSerializer(order).data)


class SiteSettingsViewSet(viewsets.ModelViewSet):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer
    permission_classes = [ReadOnlyOrAdmin]

    @action(detail=False, methods=["get"])
    def current(self, request):
        obj = SiteSettings.objects.order_by("id").first()
        if not obj:
            obj = SiteSettings.objects.create()
        return Response(self.get_serializer(obj).data)
