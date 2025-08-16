# config/urls.py
from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path, include
from products.views import (
    ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView
)

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('auth/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]
