from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products', views.products, name='products'),
    path('login', views.log_in, name='login'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('cart', views.view_cart, name='cart'),
    path('logout', views.logout, name='logout'),
    path('upload_product', views.create_product, name='upload_product'),
    path('update_cart/<int:product_id>', views.update_cart, name='update_cart'),
    path('remove_product_cart/<int:product_id>', views.remove_product_cart, name='remove_product_cart'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)