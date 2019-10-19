from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.admindash, name='dashboard'),
    path('productDetails/<product_id>', views.productDetails, name='productDetails'),
    path('productDetails/finalProduct/abc', views.finalProduct, name='finalProduct'),
    path('adminHelp/',views.adminHelp,name="adminHelp"),
    path('requestadmin/',views.requestAdmin,name='requestadmin'),
]
