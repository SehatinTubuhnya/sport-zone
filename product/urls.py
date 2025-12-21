from django.urls import path
from product.views import create_products, show_product_detail, show_json_by_id, edit_products, delete_products, show_products_list, show_json

import product.views as views

app_name = 'product'

urlpatterns = [
    path('', show_products_list, name='show_products_list'),
    path('create-products/', create_products, name='create_products'),
    path('<str:id>/', show_product_detail, name='show_product_detail'),
    path('json/<str:products_id>/', show_json_by_id, name='show_json_by_id'),
    path('<uuid:id>/edit', edit_products, name='edit_products'),
    path('<uuid:id>/delete', delete_products, name='delete_products'),
    path('json/', show_json, name='show_json'),

    path('api/products/', views.product_api_view, name='api-product-list'),
    path('api/products/create/', views.product_create_view, name='api-product-create'),
    path('api/products/<int:pk>/', views.product_detail_view, name='api-product-detail'),
    path('api/products/<int:pk>/update/', views.product_update_view, name='api-product-update'),
    path('api/products/<int:pk>/delete/', views.product_delete_view, name='api-product-delete'),

]
