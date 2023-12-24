from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('category/<int:pk>/', ProductListByCategory.as_view(), name='category'),
    path('product/<int:pk>/', product_view, name='product'),
    path('add_product/', NewProduct.as_view(), name='add_product'),
    path('product/<int:pk>/update/', ProductUpdate.as_view(), name='update'),
    path('product/<int:pk>/delete/', ProductDelete.as_view(), name='delete'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('search/', SearchResults.as_view(), name='search'),
    path('register/', register_user, name='register'),
    path('save-comment/<int:pk>/', save_comment, name='save_comment'),
    path('profile/<int:pk>/', profile_view, name='profile'),
    path('change_account/', edit_account_view, name='change_account'),
    path('change_profile/', edit_profile_view, name='change_profile'),
    path('about/creator', about_creater, name='about_creator'),
    path('about_site', about_site, name='about_site'),
    path('add_favorite/<int:pk>/', save_favorite_products, name='add_favorite'),
    path('favorite/', FavoriteProductView.as_view(), name='favorite'),
    path('cart/', cart, name='my_cart'),
    path('to_cart/<int:product_id>/<str:action>/', to_cart, name='to_cart'),
    path('clear_cart/', clear_cart, name='clear_cart'),
    path('checkout/', checkout, name='checkout'),
    path('payment/', create_checkout_session, name='payment'),
    path('success/', success_payment, name='success'),

]
