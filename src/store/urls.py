from django.urls import path
from src.store import views

urlpatterns = [
    # CATEGORY MANAGEMENT API
    path("categories", views.CategoryCreate.as_view(), name="create_category"),
    path("categories/<int:pk>", views.CategoryDelete.as_view(), name="delete_category"),
    # PRODUCT MANAGEMENT API
    path("products", views.ProductCreate.as_view(), name="create_product"),
    path("products/<int:pk>", views.ProductUpdate.as_view(), name="update_product"),
    path("products/delete/<int:pk>", views.ProductDelete.as_view(), name="delete_product"),
    path("products/filter/<min_price>/<max_price>", views.ProductFilterList.as_view(), name="list_product"),
    path("products/search", views.ProductSearchList.as_view(), name="search_product"),
]
