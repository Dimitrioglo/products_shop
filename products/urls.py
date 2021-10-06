from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.products_list, name='products-api'),
    path('products/<int:pk>/', views.products_detail),
    path('product/specification/<int:specification_id>', views.product_specification),
]
