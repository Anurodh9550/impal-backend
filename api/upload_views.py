import cloudinary.uploader
from django.conf import settings
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView


class ImageUploadView(APIView):
    """Admin-only image upload. Sends the file to Cloudinary and returns its URL."""

    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get("file") or request.FILES.get("image")
        if not file_obj:
            return Response({"detail": "No file provided. Use field name 'file'."}, status=400)

        if not getattr(settings, "CLOUDINARY_ENABLED", False):
            return Response(
                {"detail": "Cloudinary is not configured on the server."},
                status=503,
            )

        try:
            result = cloudinary.uploader.upload(
                file_obj,
                folder=settings.CLOUDINARY_UPLOAD_FOLDER,
                resource_type="image",
            )
        except Exception as exc:  # noqa: BLE001
            return Response({"detail": f"Upload failed: {exc}"}, status=502)

        return Response(
            {
                "url": result.get("secure_url"),
                "public_id": result.get("public_id"),
                "width": result.get("width"),
                "height": result.get("height"),
                "format": result.get("format"),
            }
        )
