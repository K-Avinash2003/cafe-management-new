
from django.contrib import admin

from app.models import CartItem, Order, OrderItem, Reservation, Table, User, coffeemenu

# Register your models here.
admin.site.register(User)
admin.site.register(coffeemenu)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Table)
admin.site.register(Reservation)