from django.db import models
from django.urls import reverse
import uuid # Required for unique book instances


# Create your models here.

## if not primary key, automatically add artificial one (id)


class Genre(models.Model):
    """Book genre"""

    # Fields
    name = models.CharField(
        max_length=20,
        help_text='Enter book genre',
        unique=True)

    # Methods
    # required
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('genre-detail', args=[str(self.id)])  # url mapping genre-detail should be defined + view + template




class Book(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    title = models.CharField(max_length=200, help_text='Enter book title')
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True) # auteur ne peut pas être supp si assigné à un livre
        # NB: par défaut on_delete=models.CASCADE (si auteur supprimé book aussi)
        # on pourrait aussi avoir PROTECT ou SET_NULL pour éviter suppression intempestive

    # Foreign Key used because book can only have one author, but authors can have multiple books.
    # Author as a string rather than object because it hasn't been declared yet in file. (donc déclaration string explicite)

    summary = models.TextField(max_length=500, help_text='Enter book summary',blank=True,null=True)
    isbn = models.CharField('ISBN',  # sinon serait par défaut Isbn
                            max_length=13,
                            unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(
        Genre, help_text="Select a genre for this book")

    language = models.ManyToManyField("Language",help_text="Select a language for this book")



    # Metadata
    class Meta:
        # default ordering of records when you query this model type (prefix - to revert order)
        ordering = ['title']

    # Methods
    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = 'Genre'

    # required
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""

    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,  # allocation auto valeur unique pour clé
                          help_text="Unique ID for this particular book across whole library")

    book =  models.ForeignKey(Book,on_delete=models.RESTRICT, null=True)
    due_back = models.DateField(null=True, blank=True)   # blank/null nécessaire quand book dispo
    imprint = models.CharField(max_length=200)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status = models.CharField(max_length=1,
                              help_text='Enter book status',
                              blank=True,   # don t have to fill genre
                              choices=LOAN_STATUS,
                              default="m")  # car book pas disponible avant d'être stockés


    imprint = models.CharField(max_length=20, help_text='Enter field documentation')
    #language = models.CharField(max_length=20, help_text='Enter field documentation')


    # Metadata
    class Meta:
        ordering = ['due_back']

    # Methods

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'



class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)  # null => stocke blank value as null, blank => autorise blank values
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'


class Language(models.Model):
    """Model representing the original language of a book"""   # class better than list as it may evolve (contrary to LOAN_STATUS)
    name = models.CharField(max_length=100,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)",
                            unique=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of Language."""
        return reverse('language-detail', args=[str(self.id)])  # url mapping language-detail should be defined + view + template

