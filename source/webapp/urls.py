from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (IndexView)


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]