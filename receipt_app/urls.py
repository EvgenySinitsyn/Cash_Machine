from django.urls import path
from .views import api_receipt
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('cash_machine/', api_receipt, name='receipt'),
 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)