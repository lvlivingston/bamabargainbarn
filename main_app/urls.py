from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	
urlpatterns = [
	path('', views.products, name='products'),
	path('products/', views.products, name='products'),
	path('cart/', views.cart, name='cart'),
    path('products/<int:product_id>/', views.product_detail, name='product'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/', views.update_quantity, name='update_quantity'),
    path('cart/delete/<int:product_id>/', views.delete_item, name='delete_item'),
	# path('profile/', views.profile, name='profile'),
    # path('finches/create/', views.FinchCreate.as_view(), name='finches_create'),
    # path('finches/<int:pk>/update/', views.FinchUpdate.as_view(), name='finches_update'),
    # path('finches/<int:pk>/delete/', views.FinchDelete.as_view(), name='finches_delete'),
    # path('finches/<int:finch_id>/add_feeding/', views.add_feeding, name='add_feeding'),
    # path('finches/<int:finch_id>/add_photo/', views.add_photo, name='add_photo'),
    # path('finches/<int:finch_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name='assoc_toy'),
    # path('finches/<int:finch_id>/unassoc_toy/<int:toy_id>/', views.unassoc_toy, name='unassoc_toy'),
    # path('toys/', views.ToyList.as_view(), name='toys_index'),
    # path('toys/<int:pk>/', views.ToyDetail.as_view(), name='toys_detail'),
    # path('toys/create/', views.ToyCreate.as_view(), name='toys_create'),
    # path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toys_update'),
    # path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toys_delete'),
    # path('accounts/signup/', views.signup, name='signup'),
]

# Serve media files in development
if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)