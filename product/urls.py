from django.urls import path
from product.views import create_products, show_products, show_json_by_id

app_name = 'product'

urlpatterns = [
    path('create-products/', create_products, name='create_products'),
    path('products/<str:id>/', show_products, name='show_products'),
    path('products/json/<str:products_id>/', show_json_by_id, name='show_json_by_id'),
]
