from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.upload_views import ImageUploadView
from api.views import (
    CategoryViewSet,
    EnquiryViewSet,
    GalleryItemViewSet,
    OrderViewSet,
    ProductViewSet,
    SiteSettingsViewSet,
    TestimonialViewSet,
)

router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("products", ProductViewSet)
router.register("gallery", GalleryItemViewSet)
router.register("testimonials", TestimonialViewSet)
router.register("enquiries", EnquiryViewSet)
router.register("orders", OrderViewSet)
router.register("settings", SiteSettingsViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/upload/", ImageUploadView.as_view(), name="image_upload"),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
