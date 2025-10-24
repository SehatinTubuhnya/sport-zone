from django.urls import path
from product.views import create_products, show_products, show_json_by_id, edit_products, delete_products, show_products_list

import product.views as views

app_name = 'product'

urlpatterns = [
    path('', show_products_list, name='show_products_list'),
    path('create-products/', create_products, name='create_products'),
    path('products/<str:id>/', show_products, name='show_products'),
    path('products/json/<str:products_id>/', show_json_by_id, name='show_json_by_id'),
    path('products/<uuid:id>/edit', edit_products, name='edit_products'),
    path('products/<uuid:id>/delete', delete_products, name='delete_products'),

    # 1. URL untuk halaman (yang me-load HTML)
    # path('products/', views.product_list_page_view, name='product-list-page'), 
    
    # 2. URL API untuk mengambil DAFTAR produk (GET)
    path('api/products/', views.product_api_view, name='api-product-list'),
    
    # 3. URL API untuk MEMBUAT produk (POST)
    path('api/products/create/', views.product_create_view, name='api-product-create'),
    
    # 4. URL API untuk GET detail produk (GET)
    path('api/products/<int:pk>/', views.product_detail_view, name='api-product-detail'),

    # 5. URL API untuk UPDATE produk (POST)
    path('api/products/<int:pk>/update/', views.product_update_view, name='api-product-update'),
    
    # 6. URL API untuk DELETE produk (POST)
    path('api/products/<int:pk>/delete/', views.product_delete_view, name='api-product-delete'),
]
