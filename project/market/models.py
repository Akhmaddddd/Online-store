from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название категории')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категория'


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Нaзвание продукта')
    content = models.TextField(verbose_name='Описание продукта')
    photo = models.ImageField(upload_to='photos/', default='Нет фото', verbose_name='Картинка продукта')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата выполнения')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    price = models.FloatField(verbose_name='Цена')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Владелец')

    quantity = models.IntegerField(default=0,verbose_name='Количчество')
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', kwargs={'pk': self.pk})

    def get_photo(self):
        try:
            return self.photo.url
        except:
            return 'https://www.bargas.ru/upload/iblock/eee/eee48035c2ba7dc2d95b2e3f410f6802.jpg'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Коментатор')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    text = models.CharField(max_length=400, verbose_name='Коментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата коментария')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Профиль')
    photo = models.ImageField(upload_to='profile', blank=True, null=True, verbose_name='Фото профиля')

    phone=models.CharField(max_length=40,blank=True,null=True,default='Нет номера', verbose_name='Телефонный номер')
    address = models.CharField(max_length=100, blank=True, null=True, default='Нет адреса', verbose_name='Адрес')
    publisher = models.BooleanField(default=True, verbose_name='Право добавление продукта')

    def __str__(self):
        return self.user.username

    def get_photo(self):
        try:
            return self.photo.url
        except:
            return 'https://bootdey.com/img/Content/avatar/avatar7.png'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Покупатель')
    first_name = models.CharField(max_length=250, default='', verbose_name='Имя пользователя')
    last_name = models.CharField(max_length=250, default='', verbose_name='Фамилия пользователя')

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Покупатель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    is_completed = models.BooleanField(default=False, verbose_name='Выполнен ли заказ')
    shipping = models.BooleanField(default=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    @property
    def get_cart_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([product.get_total_price for product in order_products])
        return total_price

    @property
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = sum([product.quantity for product in order_products])
        return total_quantity


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='Продукт')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='Заказ')
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name='Количество товара')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказов'

    @property
    def get_total_price(self):
        total_price = self.product.price * self.quantity
        return total_price


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, verbose_name='Покупатель')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='Заказ')
    address = models.CharField(max_length=300, verbose_name='Адрес доставки')
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True, verbose_name='Город')
    region = models.CharField(max_length=250, verbose_name='Регион')
    phone = models.CharField(max_length=250, verbose_name='Номер телефона')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата доставки')

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставок'


class City(models.Model):
    city = models.CharField(max_length=300, verbose_name='Название города')

    def __str__(self):
        return self.city

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class SaveOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Покупатель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    total_price = models.FloatField(default=0, verbose_name='Сумма заказа')

    def __str__(self):
        return f'Заказ номер : {self.pk}'

    class Meta:
        verbose_name = 'История заказа'
        verbose_name_plural = 'Истории заказа'


class SaveOrderProducts(models.Model):
    order = models.ForeignKey(SaveOrder, on_delete=models.CASCADE, null=True, related_name='products')
    product = models.CharField(max_length=300, verbose_name='Продукт')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    product_price = models.FloatField(verbose_name='Цена продукта')
    final_price = models.FloatField(verbose_name='На сумму')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата покупки')
    photo = models.ImageField(upload_to='images/', verbose_name='Фото товара')

    def get_photo(self):
        try:
            return self.photo.url

        except:
            return ''

    def __str__(self):
        return f'{self.product}'

    class Meta:
        verbose_name = 'История заказанного товара'
        verbose_name_plural = 'Истории заказаннфх товаров'
