from django.shortcuts import render   # render generate HTML file from template + data

# Create your views here.
## view : processes an HTTP request, fetches the required data from the database, renders the data in an HTML page
# using an HTML template, and then returns the generated HTML in an HTTP response to display the page to the user

from .models import Book, Author, BookInstance, Genre

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Number of genres
    num_genres = Genre.objects.count()

    # Books containing a certain word
    my_word = "dahlia"
    num_books_with_word = Book.objects.filter(title__contains=my_word).count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_with_word':num_books_with_word,
        'sought_word': my_word
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)  # original request, template html with placeholders, context variables to replace placeholders
