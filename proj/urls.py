"""
URL configuration for proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from app.views import  about, add_coffeemenu, add_to_cart, add_user, adminindex, delete_from_cart, delete_item, delete_order, delete_reservation, delete_reservations, delete_user, employeeindex, item_orders, items, login_view, logout_view, make_reservation, manageProfile, mark_as_paid, order_bill, order_list, orders, paid, place_order, register,index, reservation_list, search_items, search_order, search_orders, search_ordersname, search_products, table_list, tables, toggle_availability, toggle_status, update_item, update_reservation, update_user, user_list, view_cart

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',index,name='index'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('register/',register,name='register'),
    path('add-to-cart/<int:product_id>', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('about/',about,name="about"),
    path('delete-from-cart/<int:cart_item_id>/', delete_from_cart, name='delete_from_cart'),
    path('place-order/', place_order, name='place_order'),
    path('employeeindex/',employeeindex,name='employeeindex'),
    path('delete-order/<int:order_id>/', delete_order, name='delete_order'),
    path('admin/add-user/', add_user, name='add_user'),
    path('adminindex/',adminindex,name='adminindex'),
    path("add_user/",add_user,name="add_user"),
    path('add_coffeemenu/', add_coffeemenu, name='add_coffeemenu'),
    path('items/',items, name='items'),
    path('delete_item/<int:item_id>',delete_item,name="delete_item"),
    path('user_list/',user_list,name="user_list"),
    path('delete_user/<int:user_id>/',delete_user, name='delete_user'),
    path('update_user/<int:user_id>/',update_user,name="update_user"),
    path('update_item/<int:item_id>/',update_item,name="update_item"),
    path('orders/',orders,name="orders"),
    path('order/<int:order_id>/bill/', order_bill, name='order_bill'),
    path('delete_order/<int:order_id>/', delete_order, name='delete_order'),
    path('item_orders/',item_orders,name="item_orders"),
    path('toggle_status/',toggle_status, name='toggle_status'), 
    path('profile/<int:user_id>/',manageProfile, name='manage_profile'),
    path('order/<int:order_id>/paid/',mark_as_paid, name='mark_as_paid'),
    path('orderp/<int:order_id>/paid/', paid, name='paid'),
    path('order_list/<int:order_id>/',order_list,name="order_list"),
    path('toggle-availability/<int:item_id>/', toggle_availability, name='toggle_availability'),
    path('search/', search_products, name='search_products'),
    path('search_order/',search_order,name="search_order"),
    path('search_orders/',search_orders,name="search_orders"),
    path('search_items/',search_items,name="search_items"),
    path('search_ordersname/',search_ordersname,name="search_ordersname"),
    path('tables/', table_list, name='table_list'),
    path('reserve/', make_reservation, name='make_reservation'),
    path('reservations/', reservation_list, name='reservation_list'),
    path('delete_reservation/<int:reservation_id>/', delete_reservation, name='delete_reservation'),
    path('reserved_tables/', tables, name='tables'),
    path('update_reservation/<int:reservation_id>', update_reservation, name='update_reservation'),
    path('delete_reservations/<int:reservation_id>', delete_reservations, name='delete_reservations'),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
