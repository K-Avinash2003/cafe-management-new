from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_admin=models.BooleanField('Is admin',default=False)
    is_customer = models.BooleanField('Is customer',default=True)
    is_employee = models.BooleanField('Is employee',default=False)


class coffeemenu(models.Model):
    name = models.CharField(max_length=100)
    price=models.FloatField(default=0)
    description=models.CharField(max_length=100,default='')
    image=models.ImageField(upload_to='uploads/products/')
    available=models.BooleanField(default=True)
    def __str__(self):
        return self.name
    

class CartItem(models.Model):
    product = models.ForeignKey(coffeemenu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    session_key = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'   


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(coffeemenu, through='OrderItem')
    total_price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Order {self.id}'
    
    def calculate_total_price(self):
        total = 0
        for item in self.orderitem_set.all():
            total += item.product.price * item.quantity
        self.total_price = total
        self.save()

    def generate_bill(self):
        bill_details = f"Bill for Order {self.id}\n"
        bill_details += f"User: {self.user.username}\n"
        bill_details += f"Date: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        bill_details += "\nItems:\n"
        for item in self.orderitem_set.all():
            bill_details += f"{item.quantity} x {item.product.name} @ {item.product.price} each = {item.product.price * item.quantity}\n"
        bill_details += f"\nTotal Price: {self.total_price}\n"
        return bill_details

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(coffeemenu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.quantity} of {self.product.name} in Order {self.order.id}'    


class Table(models.Model):
    table_number = models.PositiveIntegerField(unique=True)
    res=models.BooleanField(default=False)

    def __str__(self):
        return f"Table {self.table_number}"

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    reservation_time = models.DateTimeField()
    is_reserved = models.BooleanField(default=True)

    def __str__(self):
        return f"Reservation by {self.user.username} for {self.table} at {self.reservation_time}"      
    