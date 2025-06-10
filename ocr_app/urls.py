from django.urls import path
from .views import ReceiptUploadAPIView

urlpatterns = [
    path('api/', ReceiptUploadAPIView.as_view(), name='receipt_upload_api'),
]