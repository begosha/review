from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (IndexView, ProductView, ProductCreateView, ProductDeleteView, ProductUpdateView, ReviewCreate, ReviewDeleteView, ReviewUpdateView, ReviewListView)


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/product', ProductView.as_view(), name='product'),
    path('add/', ProductCreateView.as_view(), name='product-add'),
    path('<int:pk>/update', ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/delete', ProductDeleteView.as_view(), name='product-delete'),
    path('<int:pk>/review/add', ReviewCreate.as_view(), name='review-add'),
    path('<int:pk>/review/delete', ReviewDeleteView.as_view(), name='review-delete'),
    path('<int:pk>/review/update', ReviewUpdateView.as_view(), name='review-update'),
    path('reviews-list', ReviewListView.as_view(), name='review-list')
]