from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .utils import CartForAuthenticatedUser, get_cart_data
from .models import *
from .forms import ProductForm, LoginForm, RegisterForm, CommentForm, EditAccountForm, EditProfileForm,CustomerForm,ShippingForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from project import settings
import stripe

# Create your views here.

# def index(request):
#
#     products=Product.objects.all()
#
#
#     context={
#         'title':'Главная страница: UZMarket',
#         'products':products
#     }
#
#
#
#     return render(request,'market/index.html',context)


class ProductListView(ListView):
    model = Product
    template_name = 'market/index.html'
    context_object_name = 'products'
    extra_context = {
        'title': 'Главная страница: UZMarket'
    }


# def category_view(request,pk):
#     products=Product.objects.filter(category_id=pk)
#     category=Category.objects.get(pk=pk)
#
#
#
#     context={
#         'title':f'Продукты: {category.title}',
#         'products':products
#     }
#
#
#
#     return render(request,'market/index.html',context)


class ProductListByCategory(ProductListView):
    def get_queryset(self):
        products = Product.objects.filter(category_id=self.kwargs['pk'])
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = f'Продукты: {category.title}'
        return context


def product_view(request, pk):
    product = Product.objects.get(pk=pk)
    products = Product.objects.all()[::-1][:4]

    context = {
        'title': f'Продукт: {product.title}',
        'product': product,
        'products': products,

    }
    context['comments'] = Comment.objects.filter(product=product)

    if request.user.is_authenticated:  # Если пользователь Авторизован он сможет оставлять комент
        context['form'] = CommentForm()
    return render(request, 'market/market_detail.html', context)


# def add_product(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             product = Product.objects.create(**form.cleaned_data)
#             product.save()
#
#             return redirect('product', product.pk)
#
#     else:
#         form = ProductForm()
#
#     context = {
#         'title': f'Добавление продукта',
#         'form': form
#     }
#     return render(request, 'market/add_product.html', context)


class NewProduct(CreateView):
    form_class = ProductForm
    template_name = 'market/add_product.html'
    extra_context = {
        'title': f'Добавление продукта'

    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProductUpdate(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'market/update_product.html'
    extra_context = {
        'title': f'Изменить продукт'

    }


class ProductDelete(DeleteView):
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('index')


def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            if user:
                login(request, user)
                messages.success(request, 'Вы вошли в аккаунт')
                return redirect('index')
            else:
                messages.error(request, 'Не верный логин или пароль')
                return redirect('login')

        else:
            messages.error(request, 'Не верный логин или пароль')

            return redirect('login')
    else:
        login_form = LoginForm()

    context = {
        'title': 'Вход в аккаунт',
        'login_form': login_form
    }
    if not request.user.is_authenticated:
        return render(request, 'market/login.html', context)
    else:
        return redirect('index')


def user_logout(request):
    logout(request)

    messages.warning(request, 'Вы вышли из аккаунта')
    return redirect('index')


class SearchResults(ProductListView):
    def get_queryset(self):
        word = self.request.GET.get('q')
        products = Product.objects.filter(title__icontains=word)
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        word = self.request.GET.get('q')
        context['q_name'] = word
        return context


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            profile = Profile.objects.create(user=user)
            profile.save()
            messages.success(request, 'Регистрация прошла успешно')
            return redirect('login')
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
                return redirect('register')
    else:
        form = RegisterForm()

    context = {
        'title': 'Регистрация',
        'form': form
    }
    if not request.user.is_authenticated:
        return render(request, 'market/register.html', context)
    else:
        return redirect('index')


def save_comment(request, pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.product = Product.objects.get(pk=pk)
        comment.user = request.user
        comment.save()
        messages.success(request, 'Коментарий отправлен')
        return redirect('product', pk)


def profile_view(request, pk):
    profile = Profile.objects.get(user_id=pk)
    recent_products = Product.objects.filter(author_id=pk)[::-1][:2]
    products = Product.objects.filter(author_id=pk)

    context = {
        'title': f'Профиль пользователя {profile.user.username}',
        'profile': profile,
        'recent_products': recent_products,
        'products': products
    }
    return render(request, 'market/profile.html', context)


def edit_account_view(request):
    if request.method == 'POST':
        edit_account_form = EditAccountForm(request.POST, instance=request.user)
        if edit_account_form.is_valid():
            data = edit_account_form.cleaned_data
            user = User.objects.get(id=request.user.id)
            if user.check_password(data['old_password']):  # Если старый пороль соответствует
                if data['old_password'] and data['new_password'] == data['confirm_password']:
                    user.set_password(data['new_password'])
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, '')
                    return redirect('profile', user.pk)
                else:
                    for field in edit_account_form.errors:  # Прохожу циклом по полям формы что бы получить ошибки полей
                        messages.error(request, edit_account_form.errors[field].as_text())  # По ключу получаю ошибки
                        return redirect('change_account')
            else:
                for field in edit_account_form.errors:  # Прохожу циклом по полям формы что бы получить ошибки полей
                    messages.error(request, edit_account_form.errors[field].as_text())  # По ключу получаю ошибки
                    return redirect('change_account')

            edit_account_form.save()
            return redirect('profile', user.pk)

    else:
        edit_account_form = EditAccountForm(instance=request.user)

    context = {
        'title': f'Изменение аккаунта: {request.user.username}',
        'edit_account_form': edit_account_form
    }

    return render(request, 'market/change.html', context)


def edit_profile_view(request):
    if request.method == 'POST':
        edit_profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if edit_profile_form.is_valid():
            edit_profile_form.save()
            messages.success(request, 'Данные профиля изменены')
            return redirect('profile', request.user.pk)
        else:
            for field in edit_profile_form.errors:  # Прохожу циклом по полям формы что бы получить ошибки полей
                messages.error(request, edit_profile_form.errors[field].as_text())  # По ключу получаю ошибки
                return redirect('change_profile')
    else:
        edit_profile_form = EditProfileForm(instance=request.user.profile)

    context = {
        'title': f'Изменение профиля: {request.user.username}',
        'edit_profile_form': edit_profile_form
    }

    return render(request, 'market/change.html', context)


def about_creater(request):
    context = {
        'title': 'О разарботчике сайта'
    }
    return render(request, 'market/about_creator.html', context)


def about_site(request):
    products = len(Product.objects.all())
    users = len(User.objects.all())
    comments = len(Comment.objects.all())
    categories = len(Category.objects.all())
    context = {
        'title': 'О  сайте',
        'products': products,
        'users': users,
        'comments': comments,
        'categories': categories
    }
    return render(request, 'market/about_site.html', context)


def save_favorite_products(request, pk):
    if request.user.is_authenticated:
        user = request.user
        product = Product.objects.get(pk=pk)
        favorite_products = FavoriteProduct.objects.filter(user=user)
        if user:
            if product in [i.product for i in favorite_products]:
                fav_product = FavoriteProduct.objects.get(user=user, product=product)
                fav_product.delete()
                messages.error(request, 'Товар удалён из Избранного')
            else:
                FavoriteProduct.objects.create(user=user, product=product)
                messages.success(request, 'Товар добавлен в Избранное')
    else:
        messages.error(request, 'Авторизуйтесь чтобы добавить в избранное')
    page = request.META.get('HTTP_REFERER', 'index')

    return redirect(page)


class FavoriteProductView(LoginRequiredMixin, ListView):
    model = FavoriteProduct
    context_object_name = 'products'
    template_name = 'market/favorite.html'
    login_url = 'index'

    def get_queryset(self):
        user = self.request.user
        fav = FavoriteProduct.objects.filter(user=user)
        products = [i.product for i in fav]
        return products



def cart(request):
    if request.user.is_authenticated:
        cart_info = get_cart_data(request)

        context = {
            'title': 'Моя корзина',
            'order': cart_info['order'],
            'products': cart_info['products']
        }
        return render(request, 'market/cart.html', context)
    else:
        messages.error(request, 'Авторизуйтесь чтобы зайти в корзину')
        return redirect('index')


def to_cart(request, product_id, action):
    if request.user.is_authenticated:
        user_cart = CartForAuthenticatedUser(request, product_id, action)

        page = request.META.get('HTTP_REFERER', 'product_list')
        return redirect(page)
    else:
        messages.success(request, 'Авторизуйтесь чтобы посмотреть корзину')
        page = request.META.get('HTTP_REFERER', 'index')
        return redirect(page)

def clear_cart(request):
    user_cart = CartForAuthenticatedUser(request)
    order = user_cart.get_cart_info()['order']
    order_products = order.orderproduct_set.all()
    for order_product in order_products:
        quantity = order_product.quantity
        product = order_product.product
        order_product.delete()
        product.quantity += quantity
        product.save()

    return redirect('my_cart')



def checkout(request):
    if request.user.is_authenticated:
        cart_info = get_cart_data(request)

        context = {
            'title': 'Оформление заказа',
            'order': cart_info['order'],
            'items': cart_info['products'],

            'customer_form': CustomerForm,
            'shipping_form': ShippingForm
        }
        return render(request, 'market/checkout.html', context)

    else:
        return redirect('index')

def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        user_cart = CartForAuthenticatedUser(request)
        cart_info = user_cart.get_cart_info()

        customer_form = CustomerForm(data=request.POST)
        if customer_form.is_valid():
            customer = Customer.objects.get(user=request.user)
            customer.first_name = customer_form.cleaned_data['first_name']
            customer.last_name = customer_form.cleaned_data['last_name']
            customer.save()

        shipping_form = ShippingForm(data=request.POST)
        if shipping_form.is_valid():
            address = shipping_form.save(commit=False)
            address.customer = Customer.objects.get(user=request.user)
            address.order = user_cart.get_cart_info()['order']
            address.save()

        total_price = cart_info['cart_total_price']
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Покупка на сайте LOFT MEBEL'
                    },
                    'unit_amount': int(total_price * 100)
                },
                'quantity': 1
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('success')),
            cancel_url=request.build_absolute_uri(reverse('checkout'))
        )
        return redirect(session.url, 303)


def success_payment(request):
    if request.user.is_authenticated:
        user_cart = CartForAuthenticatedUser(request)
        cart_info = user_cart.get_cart_info()
        order = cart_info['order']
        order_save = SaveOrder.objects.create(customer=order.customer, total_price=order.get_cart_total_price)
        order_save.save()
        order_products = order.orderproduct_set.all()
        for item in order_products:
            save_order_product = SaveOrderProducts.objects.create(order_id=order_save.pk,
                                                                  product=str(item),
                                                                  quantity=item.quantity,
                                                                  product_price=item.product.price,
                                                                  final_price=item.get_total_price,
                                                                  photo=item.product.get_photo())
            print(f'Заказаннный продукт {item} сохранен')
            save_order_product.save()

        user_cart.clear()
        messages.success(request, 'Ваша оплата прошла успешно')
        return render(request, 'market/success.html')
    else:
        messages.error(request, 'Авторизуйтесь чтобы зайти туда')
        return redirect('index')






