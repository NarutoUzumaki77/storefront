from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.products),
    path('products/<int:id>/', views.product_detail),
    path('collections/', views.collections_list),
    path('collections/<int:id>/', views.collection_details)
]