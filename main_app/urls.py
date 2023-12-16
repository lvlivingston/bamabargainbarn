from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
	
urlpatterns = [
	path('', views.products, name='products'),
	path('products/', views.products, name='products'),
	path('cart/', views.cart, name='cart'),
    path('products/<int:product_id>/', views.product_detail, name='product'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:order_item_id>/', views.update_quantity, name='update_quantity'),
    path('cart/delete/<int:order_item_id>/', views.delete_item, name='delete_item'),
    path('checkout/', views.checkout, name='checkout'),
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)