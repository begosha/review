from django.urls import path, include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView


HOMEPAGE_URL = 'products/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('webapp.urls')),
    path('', RedirectView.as_view(url=HOMEPAGE_URL, permanent=False))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
