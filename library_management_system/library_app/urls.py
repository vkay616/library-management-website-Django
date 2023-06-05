from django.urls import path, include
from . import views

urlpatterns = [
    # url path for home page
    path('', views.BooksList.as_view(), name='Home'),
    # url path for issuing the book
    path('<int:pk>/issue/', views.IssueBook.as_view(), name='IssueBook'),
    # url path for returning the book
    path('<int:pk>/return/', views.ReturnBook.as_view(), name='ReturnBook'),
    # <int:pk> is the primary key (id) to issue or return a specific book
]