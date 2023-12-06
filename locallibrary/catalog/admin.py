from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance, Language


#admin.site.register(Author)

class BooksInline(admin.TabularInline):
    model = Book
    # do not display additional
    extra=0
    can_delete = False

# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    # field displayed in author list
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

    # detailed view
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]  # tuple groups fields horizontaly

    # linked records
    inlines = [BooksInline]


# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)



class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

    # do not display additional
    extra=0

# Register the Admin classes for Book using the decorator
#admin.site.register(Book)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

    # display related book instances
    inlines = [BooksInstanceInline]


#admin.site.register(BookInstance)
# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book','status','due_back','id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {  # section title
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )






admin.site.register(Genre)

admin.site.register(Language)