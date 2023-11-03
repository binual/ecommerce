from django.urls import path
from.import views
urlpatterns=[
  path("",views.homepage,name="homepage"),  
  path('product_detail/<int:pk>',views.product_detail,name='product_detail'),
  
  
path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

 path('cart/', views.cart, name='cart'), 
 path('get_cart_item_count/', views.get_cart_item_count, name='get_cart_item_count'),
  
path('increase_quantity/<int:cart_item_id>/', views.increase_quantity, name='increase_quantity'),
path('decrease_quantity/<int:cart_item_id>/', views.decrease_quantity, name='decrease_quantity'),  
path('remove_from_cart/<int:cart_item_id>/',views.remove_from_cart, name='remove_from_cart'), 
 
 
path('userlogin/', views.userlogin, name='userlogin'),  
path('logout/', views.logout, name='logout'),     
path("verify_otp/",views.verify_otp,name="verify_otp"), 
  
  

path('checkout/', views.checkout, name='checkout'),
path('checkout_display/', views.checkout_display, name='checkout_display'), 




path('wishlist/', views.wishlist, name='wishlist'),

path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
path('delete_wishlist/<int:wishlist_id>/', views.delete_wishlist, name='delete_wishlist'),
path('payment/', views.payment, name='payment'),
path('stripe_payment/', views.stripe_payment, name='stripe_payment'),
path('success/', views.success, name='success'),

]