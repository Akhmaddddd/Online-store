from django.contrib import admin
from .models import *
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    list_display_links = ['id', 'title']

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','title','category','price','quantity','created_at')
    list_display_links = ['id','title']
    list_filter = ['category','price']



class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','user','product','created_at')
    list_display_links = ['id','user']


admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Profile)


admin.site.register(FavoriteProduct)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(ShippingAddress)
admin.site.register(City)
admin.site.register(SaveOrder)
admin.site.register(SaveOrderProducts)