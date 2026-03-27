from django.urls import include, path
from . import views


urlpatterns = [
    path('companies/create/', views.CreateCompanyView.as_view(), name='create-company'),
    path('companies/<int:pk>/', views.GetCompanyByIdView.as_view()),
    path('companies/update/', views.UpdateCompanyView.as_view()),
    path('companies/delete/', views.DeleteCompanyView.as_view()),
    path('storages/create/', views.CreateStorageView.as_view(), name='create-storage'),
    path('storages/<int:pk>/', views.GetStorageByIdView.as_view()),
    path('storages/<int:pk>/update/', views.UpdateStorageView.as_view()),
    path('storages/<int:pk>/delete/', views.DeleteStorageView.as_view()),
    path('suppliers/create/', views.CreateSupplierView.as_view(), name='create-supplier'),
    path('suppliers/list/', views.ListSuppliersView.as_view()),
    path('suppliers/<int:pk>/update/', views.UpdateSupplierView.as_view()),
    path('suppliers/<int:pk>/delete/', views.DeleteSupplierView.as_view()),
    path('supplies/create/', views.CreateSupplyView.as_view(), name='create-supply'),
    path('supplies/list/', views.ListSuppliesView.as_view()),
    path('products/add/', views.CreateProductView.as_view(), name='create-product'),
    path('products/list/', views.ListProductsView.as_view()),
    path('products/<int:pk>/', views.GetProductByIdView.as_view()),
    path('products/<int:pk>/update/', views.UpdateProductView.as_view()),
    path('products/<int:pk>/delete/', views.DeleteProductView.as_view()),
]
