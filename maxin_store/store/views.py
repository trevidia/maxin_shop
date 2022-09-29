from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout as django_logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
from .forms import CreateUserForm
from .models import Products, Cart


def index(request):
    return redirect('products')


def about(request):
    return HttpResponse("Welcome to about")


@login_required(login_url='login')
def products(request):
    store_products = Products.objects.all()
    return render(request, 'store/products.html', {"products": store_products})


def log_in(request):
    if request.user.is_authenticated:
        return redirect('products')
    request.session['items_total'] = 0
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('products')
        else:
            return render(request, 'store/login.html', {"error": "Invalid Username or Password"})

    return render(request, 'store/login.html')


def logout(request):
    if request.user.is_authenticated:
        print("yup")
        django_logout(request)
        return redirect('login')
    else:
        return redirect('products')


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('products')
    form = CreateUserForm()
    print("fish")

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'store/sign_up.html', {"errors": form.errors})

    return render(request, 'store/sign_up.html', {"form": form})


@login_required(login_url='login')
def create_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        product_quantity = request.POST.get('product_quantity')
        product_description = request.POST.get('product_description')
        image = request.FILES['product_image']
        print(request.FILES)
        product = Products(name=product_name, description=product_description,
                           price=product_price, quantity=product_quantity, image=image)
        product.save()
        return redirect('products')
    return render(request, 'store/upload_product.html')


@login_required(login_url='login')
def view_cart(request):
    try:
        cart_id = request.session['cart_id']
    except:
        cart_id = None
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
    else:
        cart = None
    return render(request, 'store/cart.html', {"cart": cart})


def update_cart(request, product_id):
    if request.method == 'POST':
        try:
            cart_id = request.session['cart_id']
        except:
            new_cart = Cart()
            new_cart.save()
            request.session['cart_id'] = new_cart.id
            cart_id = new_cart.id

        cart = Cart.objects.get(id=cart_id)

        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            pass
        except:
            pass
        if not product in cart.products.all():
            cart.products.add(product)
        new_total = 0.00
        for item in cart.products.all():
            new_total += float(item.price)
        request.session['items_total'] = cart.products.count()
        cart.total = new_total
        cart.save()
        return redirect('products')
    else:
        return HttpResponse('Method not supported')


def remove_product_cart(request, product_id):
    if request.method == 'POST':
        try:
            cart_id = request.session['cart_id']
        except:
            cart_id = None
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            product = Products.objects.get(id=product_id)
            if product in cart.products.all():
                cart.products.remove(product)
            cart.save()
            return redirect('cart')
    else:
        return HttpResponse('Method not supported')
