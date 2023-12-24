from django import template
from market.models import Category,FavoriteProduct


register=template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_favorite_products(user):
    fav = FavoriteProduct.objects.filter(user=user)
    products = [i.product for i in fav]
    return products




