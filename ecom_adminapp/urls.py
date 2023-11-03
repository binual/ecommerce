from django.urls import path
from.import views
urlpatterns=[
path('admin_dash/', views.admin_dash, name='admin_dash'),  

path('admin_login/', views.admin_login, name='admin_login'),  


path('category/', views.category, name='category'),  
path('addcategory/', views.addcategory, name='addcategory'),


path('editcategory/<int:pk>',views.editcategory,name='editcategory'),

path('deletecategory/<int:pk>',views.deletecategory,name='deletecategory'),


path('addsubcategory/', views.addsubcategory, name='addsubcategory'),
path('subcategory/', views.subcategory, name='subcategory'),

path('editsubcategory/<int:pk>',views.editsubcategory,name='editsubcategory'),

path('deletesubcategory/<int:pk>',views.deletesubcategory,name='deletesubcategory'),


path('product/', views.product, name='product'),
path('addproduct/', views.addproduct, name='addproduct'),

path('editproduct/<int:pk>/', views.editproduct, name='editproduct'),
path('deleteproduct/<int:pk>/', views.deleteproduct, name='deleteproduct'),
path('orders/', views.orders, name='orders'),



path('size/', views.size, name='size'),
path('addsize/', views.addsize, name='addsize'),
path('editsize/<int:pk>/', views.editsize, name='editsize'),
path('deletesize/<int:pk>/', views.deletesize, name='deletesize'),


path('color/', views.color, name='color'),
path('addcolor/', views.addcolor, name='addcolor'),

path('editcolor/<int:pk>/', views.editcolor, name='editcolor'),
path('deletecolor/<int:pk>/', views.deletecolor, name='deletecolor'),



]