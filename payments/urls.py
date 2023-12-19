from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views, webhooks
	
urlpatterns = [
    path('<int:order_id>/', views.checkout, name='checkout'),
    path('stripe-webhook/', webhooks.stripe_webhook, name='stripe_webhook'),
    path('<int:order_id>/pay/', views.pay, name='pay'),
    path('<int:order_id>/success/', views.success, name='success'),
    path('<int:order_id>/cancel/', views.cancel, name='cancel'),
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)