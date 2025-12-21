from django.urls import path
import product.views as views

app_name = "product"

urlpatterns = [
    path("api/products/", views.product_api_view, name="api-product-list"),
    path("api/products/create/", views.product_create_view, name="api-product-create"),
    path("api/products/<int:pk>/update/", views.product_update_view, name="api-product-update"),
    path("api/products/<int:pk>/delete/", views.product_delete_view, name="api-product-delete"),
    path("json/", views.show_json, name="show_json"),
]
