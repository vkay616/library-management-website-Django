from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# creating Book model to store books in the database
class Book(models.Model):
    # CharField to store the book's name
    name = models.CharField(max_length=250)
    # CharField to store the author's name
    author = models.CharField(max_length=250)
    # ImageField to store the book's image
    image = models.ImageField(upload_to='static/images/books', null=True) 
    #null=true, means its not necessary for a book in the database to have an image

    # TextField to store the summary/synopsis of the book
    summary = models.TextField(null=True, blank=True)
    # summary is also an optional field just like the image

    # choices for the status of book whether the book is available for issuing or someone has already issued the book
    STATUS_CHOICES = (
        ('available', ('Available for issuing')),
        ('issued', ('Issued by someone')),
    )
    # CharField to store the book's current status
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')

    issuer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # string representation of the model
    def __str__(self) -> str:
        return self.name + " | " + self.author