from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class Tag(models.Model):
    "Model representing a book tag"
    name = models.CharField(max_length=200)
    
    def __str__(self):
        "String for representing the Model object."
        return self.name

class Boogazine(models.Model):
    "Model representing a book or a magazine"
    location = models.CharField(max_length=7)
    title = models.CharField(max_length=200)
    year = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length=20, default='Book')
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    publisher = models.ForeignKey('Publisher', on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, help_text='Select a tag for this book')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        "String for representing the Model object."
        return self.title
    
    def get_absolute_url(self):
        "Returns the url to access a detail record for this book."
        return reverse('book-detail', args=[str(self.id)])
    
import uuid # Required for unique book instances

class BoogazineInstance(models.Model):
    "Model representing a specific copy of a book/magazine (i.e. that can be borrowed from the library)."
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Boogazine', on_delete=models.SET_NULL, null=True) 
    due_back = models.DateField(null=True, blank=True)
    
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
    
    LOAN_STATUS = (
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Book/Magazine availability',
    )

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"), ("can_delete_book", "Delete book"), ("can_add_book", "Add book"), ("can_edit_book", "Edit book"), ("can_reserve_book", "Reserve book"))

    def __str__(self):
        "String for representing the Model object."
        return f'{self.id} ({self.book.title})'
    
class Author(models.Model):
    "Model representing an author."
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
    
    def get_absolute_url(self):
        "Returns the url to access a particular author instance."
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        "String for representing the Model object."
        return f'{self.last_name}, {self.first_name}'
    
class Publisher(models.Model):
    "Model representing a publisher."
    name = models.CharField(max_length=100)

    def __str__(self):
        "String for representing the Model object."
        return self.name

