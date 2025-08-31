# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('products/', include('products.urls', namespace='products')),
    path('auth/', include('users.urls')),
    path('admin/', admin.site.urls),
]
