from django.urls import path

from . import views

app_name = 'ecommerce_app'
urlpatterns = [
    path('', views.allProdCategory, name='allProductCategory'),
    path('<slug:c_slug>/', views.allProdCategory, name='Products_by_Category'),
    path('<slug:c_slug>/<slug:pro_slug>/', views.proDetails, name='prodetails'),
]
