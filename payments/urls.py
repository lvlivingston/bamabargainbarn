from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views
	
urlpatterns = [
    path('cart/checkout/<int:order_id>/', views.checkout, name='checkout'),
    path('cart/checkout/pay/<int:order_id>/', views.pay, name='pay'),
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)