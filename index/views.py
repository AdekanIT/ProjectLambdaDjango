from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from . import forms
from .handlers import bot
from .models import Product, Cart, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views import View


# Create your views here.
def home(request):
    search_bar = forms.SearchForm()
    # Send elements to front
    # Get all products
    product_info = Product.objects.all()
    category_info = Category.objects.all()
    context = {'form': search_bar,
               'product': product_info,
               'category': category_info}
    return render(request, 'home.html', context)


def get_all_category(request, pk):
    category = Category.objects.get(id=pk)
    products = Product.objects.filter(category_name=category)
    # Send it to front
    context = {'products': products}
    return render(request, 'category.html', context)


# Show info about product
def get_full_product(request, pk):
    product = Product.objects.get(id=pk)
    # Send it to front
    context = {'product': product}
    return render(request, 'product.html', context)


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def search_product(request):
    if request.method == 'POST':
        get_product = request.POST.get('search_product')

        try:
            except_product = Product.objects.get(pr_name__icontains=get_product)

            return redirect(f'product/{except_product.id}')
        except:
            return redirect('/product-not-found')


def pr_not_found(request):
    return render(request, 'not_found.html')


# Add products into cart
def add_to_cart(request, pk):
    if request.method == 'POST':
        checker = Product.objects.get(id=pk)
        if checker.pr_count >= int(request.POST.get('pr_amount')):
            Cart.objects.create(user_id=request.user.id,
                                user_product=checker,
                                user_product_quantity=int(request.POST.get('pr_amount'))).save()
            return redirect('/')


# Show cart of user
def get_user_cart(request):
    # All info about user cart
    cart = Cart.objects.filter(user_id=request.user.id)

    if request.method == 'POST':
        text = 'New order!\n\n'

        for i in cart:
            text += f'Name of product: {i.user_product}\n'\
                    f'Count: {i.user_product_quantity}\n\n'
        bot.send_message(-4136629013, text)
        cart.delete()
        return redirect('/')

    # Send to front
    context = {'cart': cart}
    return render(request, 'cart.html', context)


# Delete product from cart
def del_from_cart(request, pk):
    product_to_delete = Product.objects.get(id=pk)
    Cart.objects.filter(user_id=request.user.id,
                        user_product=product_to_delete).delete()
    return redirect('/cart')


# Registration
class Register(View):
    template_name = 'registration/register.html'

    # Send form registration
    def get(self, request):
        context = {'form': UserCreationForm}
        return render(request, self.template_name, context)

    # Add user to db
    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        # context = {'form': UserCreationForm}
        # return render(request, self.template_name, context)


# func for logout
def logout_review(request):
    logout(request)
    return redirect('/')







