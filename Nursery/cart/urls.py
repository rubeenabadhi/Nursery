

from django.urls import path
from .import views

urlpatterns=[
    path('cart_detaials',views.cart_detaials,name='cart_details'),
    path('add/<int:plant_id>/', views.add_cart, name='addcart'),
    path('cart_decrement/<int:plant_id>/',views.decrement_cart, name= 'cart_decrement'),
    path('removecart/<int:plant_id>/', views.remove_cart, name='removecart'),
    path('checkout',views.checkout,name='checkout',),
    path('payments',views.payments,name='payment'),
    # path('generate_invoice', views.generate_invoice, name='generate_invoice'),
    path('success',views.success,name='success'),
    path('generate_bill/<int:checkout_id>/', views.generate_bill, name='generate_bill'),
    path('manage_checkouts/<int:admin_id>/', views.manage_checkouts, name='manage_checkouts'),

]