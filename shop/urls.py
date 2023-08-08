from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('pro/', views.pro, name='pro'),
    path('products/', views.products, name='products'),
    path('create/', views.create, name='create'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('duplicate/<int:id>/', views.duplicate, name='duplicate'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('purchase/', views.purchase, name='purchase'),
    path('BuyNow/<int:id>/', views.BuyNow, name='BuyNow'),
    path('buynow/<int:id>/', views.buynow, name='buynow'),
    path('AddToCart/<int:id>/', views.AddToCart, name='AddToCart'),
    path('Cart/', views.Cart, name='Cart'),
    path('update_quantity/', views.update_quantity, name='update_quantity'),
    path('remove/<int:id>/', views.remove_from_cart, name='remove'),
    path ('payment/', views.payments, name='payment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
