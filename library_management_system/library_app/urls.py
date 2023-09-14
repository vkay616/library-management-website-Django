from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # url path for home page
    path('', views.BooksList.as_view(), name='Home'),
    # url path for issuing the book
    path('<int:pk>/issue/', login_required(views.IssueBook.as_view()), name='IssueBook'),
    # url path for returning the book
    path('<int:pk>/return/', login_required(views.ReturnBook.as_view()), name='ReturnBook'),
    # <int:pk> is the primary key (id) to issue or return a specific book

    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('<int:pk>/', views.ViewBook.as_view(), name='ViewBook'),
]