from django.urls import path
<<<<<<< HEAD
=======

>>>>>>> 3b6aee0eacf13dc4e1e2bbdd9245fa1b8cd1a423
import product.views as views
from product.views import (
    create_products,
    delete_products,
    edit_products,
    show_json,
    show_json_by_id,
    show_product_detail,
    show_products_list,
)

app_name = "product"

urlpatterns = [
<<<<<<< HEAD
    path('api/products/', views.product_api_view, name='api-product-list'),
    path('api/products/create/', views.product_create_view, name='api-product-create'),
    path('api/products/<int:pk>/update/', views.product_update_view, name='api-product-update'),
    path('api/products/<int:pk>/delete/', views.product_delete_view, name='api-product-delete'),
    path('json/', views.show_json, name='show_json'),
=======
    path("", show_products_list, name="show_products_list"),
    path("create-products/", create_products, name="create_products"),
    path("<str:id>/", show_product_detail, name="show_product_detail"),
    path("json/<str:products_id>/", show_json_by_id, name="show_json_by_id"),
    path("<uuid:id>/edit", edit_products, name="edit_products"),
    path("<uuid:id>/delete", delete_products, name="delete_products"),
    path("json-all/", show_json, name="show_json"),
    path("api/products/", views.product_api_view, name="api-product-list"),
    path("api/products/create/", views.product_create_view, name="api-product-create"),
    path(
        "api/products/<int:pk>/", views.product_detail_view, name="api-product-detail"
    ),
    path(
        "api/products/<int:pk>/update/",
        views.product_update_view,
        name="api-product-update",
    ),
    path(
        "api/products/<int:pk>/delete/",
        views.product_delete_view,
        name="api-product-delete",
    ),
>>>>>>> 3b6aee0eacf13dc4e1e2bbdd9245fa1b8cd1a423
]
