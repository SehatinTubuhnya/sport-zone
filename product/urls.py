from django.urls import path
from product.views import create_products, show_products, show_json_by_id, edit_products, delete_products, show_products_list
app_name = 'product'

urlpatterns = [
    path('', show_products_list, name='show_products_list'),
    path('create-products/', create_products, name='create_products'),
    path('products/<str:id>/', show_products, name='show_products'),
    path('products/json/<str:products_id>/', show_json_by_id, name='show_json_by_id'),
    path('products/<uuid:id>/edit', edit_products, name='edit_products'),
    path('products/<uuid:id>/delete', delete_products, name='delete_products'),
]
