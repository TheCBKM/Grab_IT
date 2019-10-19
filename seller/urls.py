from django.urls import path, include
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('seller/',views.seller,name='seller'),
    path('buyer/',views.buyer,name='buyer'),
    path('register',views.register),
    path('login',views.login),
    path('logout/',views.logout,name='logout'),
    path('dashboard/', views.dashboard),
    path('addProduct/',views.addProduct,name='addProduct'),
    path('addProduct/category/<c_id>',views.getCategory),
    path('addProduct/subcategory/<s_id>', views.getSubCategory),
    path('seller/checkmail/<email_id>', views.checkmail),
    path('addProduct/sendProduct', views.sendProduct),
    path('seller/sellerhome',views.sellerhome),
    path('sold/<product_id>', views.sold, name='sold'),
    # Buyer
    path('buyer/',views.buyer, name='buyer'),
    path('buyer/subcategory/<cat_id>',views.subcategory, name ='subcategory'),
    path('buyer/request',views.request, name='request'),
]

