from ast import parse
import datetime
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render

from app.forms import CoffeemenuForm, LoginForm, ReservationForm, UserForm, UserFormUp, signUpForm,UserCreationForm
from django.contrib.auth import authenticate,login,logout

from app.models import CartItem, Order, OrderItem, User, coffeemenu

# Create your views here.
def index(request):
    coffees=coffeemenu.objects.all()
    return render(request, 'index.html',{"coffee":coffees})

def register(request):
    msg=None
    if request.method == 'POST':
        form =signUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            msg='user created'
            return redirect('login')
        else:
            msg='form is not valid'
    else:
        form=signUpForm()

    return render(request, 'register.html', {'form':form, 'msg':msg})

def login_view(request):
    form = LoginForm(request.POST)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_customer:
                login(request, user)
                return redirect('index')
            if user is not None and user.is_employee:
                login(request, user)
                return redirect('employeeindex')
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('adminindex')
            else:
                msg = 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form})


def employeeindex(request):
    items=OrderItem.objects.all()
    order=Order.objects.all()
    return render(request, 'employeeindex.html', {'items':items, 'orders':order})
    
def logout_view(request):
    logout(request)
    # Redirect to a page after logout, such as the login page
    return redirect('login')


def add_to_cart(request, product_id):
    product = get_object_or_404(coffeemenu, id=product_id)
    session_key = request.session.session_key
    quantity = int(request.POST.get('quantity', 1))
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_item, created = CartItem.objects.get_or_create(product=product, session_key=session_key)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity    
    cart_item.save()
    return redirect('index')

def view_cart(request):
    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(session_key=session_key)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def delete_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')


def about(request):
    items=OrderItem.objects.all()
    order=Order.objects.all()
    return render(request, 'about.html',{'items':items, 'orders':order})

from django.shortcuts import render, redirect
from .models import Reservation, Table, User, CartItem, Order, OrderItem

def place_order(request):
    session_key = request.session.session_key
    if not session_key:
        return redirect('view_cart')

    cart_items = CartItem.objects.filter(session_key=session_key)
    
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    order = Order.objects.create(user=user, total_price=0)
    
    for cart_item in cart_items:
        OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
        order.total_price += cart_item.product.price * cart_item.quantity
    order.save()
    cart_items.delete()

    return render(request, 'order_place.html',{'order': order})

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('employeeindex')

def delete_item(request, item_id):
    item = get_object_or_404(coffeemenu, id=item_id)
    item.delete()
    return redirect('items')  # Redirect to the items list page after deletion

def adminindex(request):
    return render(request, 'adminindex.html')

def add_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            return redirect('adminindex')  # Redirect to the admin index page or any other page
    else:
        form = UserCreationForm()
    
    return render(request, 'add_user.html', {'form': form})

def add_coffeemenu(request):
    if request.method == 'POST':
        form = CoffeemenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adminindex')  # Redirect to a view that lists the menu items
    else:
        form = CoffeemenuForm()
    
    return render(request, 'add_coffeemenu.html', {'form': form})


def items(request):
    # Retrieve all coffeemenu items from the database
    coffeemenu_items = coffeemenu.objects.all()

    # Render the template with the fetched items
    return render(request, 'items.html', {'coffeemenu_items': coffeemenu_items})

def user_list(request):
    users = User.objects.all()
    return render(request, 'userlist.html', {'users': users})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('user_list')  # Redirect to the user list page after deletion


def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    form = UserForm(request.POST or None, instance=user)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('user_list')  # Redirect to user list after successful update

    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'update_user.html', context)

def update_item(request, item_id):
    item = get_object_or_404(coffeemenu, id=item_id)
    form = CoffeemenuForm(request.POST or None, request.FILES or None, instance=item)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('items')  # Redirect to items list after successful update

    context = {
        'form': form,
        'item': item,
    }
    return render(request, 'update_item.html', context)

def orders(request):
    items=OrderItem.objects.all()
    order=Order.objects.all()
    return render(request, 'orders.html', {'items':items, 'orders':order})

def order_bill(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.calculate_total_price()
    order_items = order.orderitem_set.all()
    
    items_with_total = []
    for item in order_items:
        total_price = item.product.price * item.quantity
        
        
    # Calculate total price
        
        items_with_total.append({
            'product': item.product,
            'quantity': item.quantity,
            
            'total_price': total_price
        })
    
    return render(request, 'bill.html', {'order': order, 'items_with_total': items_with_total})

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('orders')


def item_orders(request):
    items = OrderItem.objects.all()
    order=Order.objects.all()
    return render(request, 'item_orders.html', {'items':items, 'orders':order})


def toggle_status(request):
    if request.method == 'POST':
        order_item_id = request.POST.get('order_item_id')
        order_item = get_object_or_404(OrderItem, id=order_item_id)
        # Toggle the status field
        order_item.status = not order_item.status
        order_item.save()
        # Redirect back to the same page or another page as needed
        return redirect('employeeindex')  # Redirect to your orders page or another suitable URL
    # Handle invalid requests or GET requests
    return redirect('employeeindex') 

def manageProfile(request,user_id):
    user = get_object_or_404(User, id=user_id)
    form = UserFormUp(request.POST or None, instance=user)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to user list after successful update

    context = {
        'form': form,
        'user': user,
    
    }
    return render(request, 'manageProfile.html', context)


def mark_as_paid(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.paid = True
    order.save()
    return redirect('orders')

def paid(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.paid = True
    order.save()
    return redirect('place_order') 

def order_list(request,order_id):
    order = get_object_or_404(Order, id=order_id)
    order.calculate_total_price()
    order_items = order.orderitem_set.all()
    
    items_with_total = []
    for item in order_items:
        total_price = item.product.price * item.quantity
        items_with_total.append({
            'product': item.product,
            'quantity': item.quantity,
            'total_price': total_price
        })
    
    return render(request, 'order_list.html', {'order': order, 'items_with_total': items_with_total})

def toggle_availability(request, item_id):
    item = get_object_or_404(coffeemenu, id=item_id)
    item.available = not item.available
    item.save()
    return redirect('items')

def search_products(request):
    query = request.GET.get('q')
    if query:
        coffee = coffeemenu.objects.filter(name__icontains=query, available=True)
    else:
        coffee = coffeemenu.objects.filter(available=True)
    
    return render(request, 'index.html', {'coffee': coffee})

def search_order(request):
    query = request.GET.get('q')
    if query:
            order = Order.objects.get(id=query)
            orders = [order]
            
    else:
        orders = Order.objects.all()
    
    return render(request, 'employeeindex.html', {'orders': orders})

def search_orders(request):
    query = request.GET.get('q')
    if query:
            order = Order.objects.get(id=query)
            orders = [order]
            
    else:
        orders = Order.objects.all()
    
    return render(request, 'item_orders.html', {'orders': orders})

def search_items(request):
    query = request.GET.get('q')
    if query:
        coffeemenu_items = coffeemenu.objects.filter(name__icontains=query)
    else:
        coffeemenu_items = coffeemenu.objects.all()
    
    return render(request, 'items.html', {'coffeemenu_items': coffeemenu_items})

from django.db.models import Q

def search_ordersname(request):
    query = request.GET.get('q', '')

    if query.isdigit():
       orders = Order.objects.filter(Q(user__username__icontains=query) | Q(id=int(query)))
    else:
       orders = Order.objects.filter(user__username__icontains=query)
    return render(request, 'orders.html', { 'orders':orders})

def table_list(request):
    tables = Table.objects.all()
    Reservations=Reservation.objects.all()
    reserved_tables = Reservation.objects.filter(is_reserved=True).values_list('table', flat=True)
    return render(request, 'table_list.html', {'tables': tables,'reserved_tables': reserved_tables})

from datetime import datetime, timezone

def make_reservation(request):
    tables = Table.objects.all()
    reserved_tables = Reservation.objects.filter(reservation_time__gte=datetime.now()).values_list('table_id', flat=True)
    
    if request.method == 'POST':
        table_id_str = request.POST.get('table')
        reservation_time_str = request.POST.get('reservation_time')
        
        
        if table_id_str and reservation_time_str:
            try:
                # Convert table_id to integer
                table_id = int(table_id_str)
                
                # Get the Table instance
                table = Table.objects.get(id=table_id)
                
                # Parse reservation_time from the ISO format
                reservation_time = datetime.strptime(reservation_time_str, '%Y-%m-%dT%H:%M')
                
                # Create and save the reservation
                reservation = Reservation(
                    user=request.user,
                    table=table,
                    reservation_time=reservation_time,
                    
                )
                reservation.save()
                
                return redirect('reservation_list')  # Redirect to a success page or reservation list
            
            except ValueError:
                # Handle the case where table_id is not a valid integer
                return render(request, 'make_reservation.html', {
                    'error': 'Invalid table ID or reservation time format.',
                    'tables': tables,
                    'reserved_tables': reserved_tables,
                })
            except Table.DoesNotExist:
                # Handle the case where the table does not exist
                return render(request, 'make_reservation.html', {
                    'error': 'Table does not exist.',
                    'tables': tables,
                    'reserved_tables': reserved_tables,
                })
    
    # If the method is not POST or if there's an error, render the form
    return render(request, 'make_reservation.html', {
        'tables': tables,
        'reserved_tables': reserved_tables,
    })
   


def reservation_list(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'reservation_list.html', {'reservations': reservations})

def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    if request.method == 'POST':
        reservation.delete()
        return redirect('reservation_list')  # Redirect to a page showing the updated list of reservations
    
    return redirect('reservation_list')

def tables(request):
    reservations = Reservation.objects.all()  # Get all reservations
    return render(request, 'tables.html', {'reservations': reservations})


def update_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('tables')
    else:
        form = ReservationForm(instance=reservation)
    
    return render(request, 'update_reservation.html', {'form': form, 'reservation': reservation})


def delete_reservations(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    if request.method == 'POST':
        reservation.delete()
        return redirect('tables')
    
    return render(request, 'confirm_delete.html', {'reservation': reservation})
