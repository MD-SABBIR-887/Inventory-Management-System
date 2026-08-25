from django.contrib import admin
from inventory.models import CustomUser,UserProfile,Invoice,CustomerCategory,Customer,Product
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(Customer)
admin.site.register(CustomerCategory)
admin.site.register(Product)
admin.site.register(Invoice)
