from django.contrib import admin
from .models import Category,Expense
from .models import UserProfile

admin.site.register(Category)
admin.site.register(Expense)