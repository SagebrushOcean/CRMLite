from django.urls import include, path
from . import views


urlpatterns = [
    path('companies/create/', views.CreateCompanyView.as_view(), name="create-company"),
    path("companies/<int:pk>/", views.RetrieveCompanyView.as_view()),
    path("companies/update", views.UpdateCompanyView.as_view()),
    path("companies/delete", views.DeleteCompanyView.as_view()),
    path('storages/create/', views.CreateStorageView.as_view(), name="create-storage"),
    path("storages/<int:pk>/", views.RetrieveStorageView.as_view()),
    path("storages/<int:pk>/update", views.UpdateStorageView.as_view()),
    path("storages/<int:pk>/delete", views.DeleteStorageView.as_view()),
#   path("create/", CreateProductView.as_view(), name="create-product"),
]
