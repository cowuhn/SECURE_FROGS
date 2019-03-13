from django.shortcuts import render
from catalog.models import Tag, Boogazine, BoogazineInstance, Author, Publisher
from django.views import generic

# Create your views here.

def index(request):
    "View function for home page of site."

    # Generate counts of some of the main objects
    num_boogazines = Boogazine.objects.all().count()
    num_instances = BoogazineInstance.objects.all().count()
    
    # Available books (status = 'a')
    num_instances_available = BoogazineInstance.objects.filter(status__exact='a').count()
    
    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()
    num_publishers = Publisher.objects.count()
    
    context = {
        'num_boogazines': num_boogazines,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_publishers' : num_publishers,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Boogazine

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['book_list'] = Boogazine.objects.all()
        context['book_books'] = Boogazine.objects.filter(type="Book")
        context['book_instance'] = BoogazineInstance.objects.filter(status='a')

        return context

    template_name = 'all_books'