from django.urls import path
from .views import get_products, product, create_product, update_product, delete_product, get_categories, create_category

urlpatterns = [
    path('', get_products,),
    path('<int:pk>/', product),
    path('create/', create_product),
    path('<int:pk>/update/', update_product),
    path('<int:pk>/delete/', delete_product),
    path('categories/', get_categories),
    path('categories/create/', create_category),
]