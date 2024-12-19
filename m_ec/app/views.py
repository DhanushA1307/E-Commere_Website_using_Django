from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from . models import Product, Customer, Cart, Payment, OrderPlaced, Wishlist, OrderPlaced
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
import random
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
def home(request):
    totalitem = 0
    totalamount = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))    
    return render(request,"app/home.html", locals())

def about(request):
    totalitem = 0
    totalamount = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
    return render(request,"app/about.html",locals())

def contact(request):
    totalitem = 0
    totalamount = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
    return render(request,"app/contact.html", locals())

class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        totalitem = 0
        totalamount = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
        return render(request, "app/category.html", locals())
    
class CategoryTitle(View):
    def get(self, request, val):
        title = Product.objects.filter(category=product[0].category).values('title')
        product = Product.objects.filter(title=val)
        totalitem = 0
        totalamount = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
        return render(request, "app/category.html", locals())

class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        totalitem = 0
        totalamount = 0
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(product = product))
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
        return render(request, "app/productdetail.html",locals())
    
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem = 0
        totalamount = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
        return render(request, "app/customerregistration.html", locals())
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Register Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, "app/customerregistration.html", locals())
    
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = 0
        totalamount = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
        return render(request, "app/profile.html", locals())
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user = user, name = name, locality = locality, city = city, mobile = mobile, state = state, zipcode = zipcode)
            reg.save()
            messages.success(request,"Congratulations! Profile Save Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, "app/profile.html", locals())
    
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    totalamount = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))    
    return render(request,"app/address.html", locals())

class updateAddress(View):
    def get(self, request, pk):
        add=Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        totalamount = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
        return render(request, "app/updateAddress.html", locals())
    
    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations! Profile Updated Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")

def custom_logout_view(request):
    logout(request)
    return render(request,'app/home.html', locals())

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        prod_id = request.POST.get('prod_id')
        product = get_object_or_404(Product, id=prod_id)
        
        cart_item, created = Cart.objects.get_or_create(
            product=product,
            user=request.user,  # Assuming you have a user field to track the cart items
        )
        
        if not created:
            messages.success(request, 'The product is already in your cart.')
        else:
            messages.info(request, 'Product added to cart successfully.')

        return redirect('/cart')

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discount_price
        amount += value
    totalamount = amount+40
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))   
    return render(request, 'app/addtocart.html',locals())

class CheckoutView(LoginRequiredMixin, View):
    login_url = ''  # Optional: specify the login URL
    redirect_field_name = 'redirect_to'  # Optional: specify the redirect field name

    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        totalitem = len(cart_items) if user.is_authenticated else 0
        famount = sum(item.quantity * item.product.discount_price for item in cart_items)
        totalamount = famount + 40 if famount > 40 else 0
        razoramount = totalamount * 100

        payment_id = 'mens_cloth' + str(random.randint(111111111, 999999999))
        while Payment.objects.filter(razorpay_payment_id=payment_id).exists():
            payment_id = 'mens_cloth' + str(random.randint(111111111, 999999999))

        payment = Payment(
            user=user,
            amount=totalamount,
            razorpay_payment_id=payment_id
        )
        payment.save()

        context = {
            'add': add,
            'cart_items': cart_items,
            'totalamount': totalamount,
            'payment_id': payment_id,
            'razoramount': razoramount
        }
        return render(request, 'app/checkout.html', context)

@csrf_exempt
def payment_done(request):
    cust_id = request.GET.get('cust_id')
    customer = Customer.objects.get(id=cust_id)
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    payment_id = request.GET.get('payment_id')
    payment = Payment.objects.get(razorpay_payment_id=payment_id)
    
    for item in cart_items:
        OrderPlaced.objects.create(
            user=user,
            product=item.product,
            quantity=item.quantity,
            customer=customer,
            payment=payment,
            total_cost=item.quantity * item.product.discount_price
        )
        item.delete()
    
    return redirect('orders')

@login_required
def orders(request):
    # totalitem = len(Cart.objects.filter(user=request.user)) if request.user.is_authenticated else 0
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed': order_placed})

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discount_price
            amount += value
        totalamount = amount+40
        if(totalamount == 40):
            totalamount = 0
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discount_price
            amount += value
        totalamount = amount+40
        if(totalamount == 40):
            totalamount = 0
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discount_price
            amount += value
        totalamount = amount+40
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user = user, product=product).save()
        data = {
            'message':'Wishlist Added Successfullly',
        }
        return JsonResponse(data)
    
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user = user, product=product).delete()
        data = {
            'message':'Wishlist Remove Successfullly',
        }
        return JsonResponse(data)