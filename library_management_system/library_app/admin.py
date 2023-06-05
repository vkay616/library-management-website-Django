from django.contrib import admin
from .models import Book
# Register your models here.

# registering the Book model to admin panel
admin.site.register(Book)