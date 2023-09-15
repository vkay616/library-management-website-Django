# importing the required libaries
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import Book
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout

# Create your views here.
def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("Home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render(request, template_name="library_app/register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("Home")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="library_app/login.html", context={"login_form":form})


def logout_view(request):
    logout(request)
    return redirect("Home")


# a class based view for the home page
# a ListView is used to list all the objects of the specified model
class BooksList(ListView):
    # specifying the model for the ListView
    model = Book
    # using a custom template name instead of the default
    template_name = 'library_app/books.html'

    # function used for passing extra content to the template
    def get_context_data(self, **kwargs):
        context = super(BooksList, self).get_context_data(**kwargs)
        # filtering and storing all the books having 'available' status in the available_books variable
        available_books = Book.objects.filter(status__startswith='a')
        # adding the list of available books to the context dictionary
        context['available_books'] = available_books
        # number of available books
        available_books_count = available_books.count()
        # adding the number of available books to context dictionary
        context['available_books_count'] = available_books_count
        # filtering and storing all the issued books in issued_books variable
        if self.request.user.is_authenticated:
            issued_books = Book.objects.filter(issuer=self.request.user)
        else:
            issued_books = None
        # adding the list of issued books to context dictionary
        context['issued_books'] = issued_books
        # returning the modified context dictionary to the template
        return context

# a class based view for issuing the book
# an UpdateView is used for easily updating/modifying a particular object of the model
class IssueBook(UpdateView):
    # specifying the model
    model = Book
    # the list of fields that would be included in the form is empty
    # as we're only switching the 'status' of the book from available to issued.
    fields = ['issuer']
    # using a custom template name for the view
    template_name = 'library_app/issue_return.html'

    # function to deal with the POST request and accepts two parameters - request and pk (id)
    def post(self, request, pk):
        # getting the particular book using its id (primary key)
        book = Book.objects.get(id=pk)
        # only switch the 'status' of the book if a POST request is sent
        if request.method == "POST":
            # changing the 'status' of the book from available to issued
            book.status = "Issued by someone"
            book.issuer = request.user
            # save the change
            book.save()
            # after successfully changing redirect back to home page
            return redirect('Home')
    # function used to pass extra content to the template
    def get_context_data(self, **kwargs):
        context = super(IssueBook, self).get_context_data(**kwargs)
        # passing a 'type' since I used the same template (html file) for issuing and returning
        context['type'] = 'issue'
        # returning modified context dictionary
        return context

# class based view for returning book
# an UpdateView is used for easily updating/modifying a particular object of the model
class ReturnBook(UpdateView):
    # specifying the model for the view
    model = Book
    # the list of fields that would be included in the form is empty
    # as we're only switching the 'status' of the book from available to issued.
    fields = ['issuer']
    # using a custom template name for the view
    template_name = 'library_app/issue_return.html'

    # function to deal with POST request and accepts two parameters - request and pk (id)
    def post(self, request, pk):
        # getting the particular book using its id (primary key)
        book = Book.objects.get(id=pk)
        # only switch the 'status' of the book if a POST request is sent
        if request.method == "POST":
            # changing the 'status' of the book from issued to available
            book.status = "Available for issuing"
            book.issuer = None
            # save the change
            book.save()
            # after successfully changing redirect back to home page
            return redirect('Home')

class ViewBook(ListView):
    # specifying the model
    model = Book
    # using a custom template name for the view
    template_name = 'library_app/view_book.html'


    # function used to pass extra content to the template
    def get_context_data(self, **kwargs):
        context = super(ViewBook, self).get_context_data(**kwargs)

        book = Book.objects.get(id=self.kwargs['pk'])

        context['book'] = book

        # returning modified context dictionary
        return context