from django.contrib import admin
from catalog.models import Tag, Boogazine, BoogazineInstance, Author, Publisher

# Register your models here.

admin.site.register(Tag)
admin.site.register(Boogazine)
admin.site.register(BoogazineInstance)
admin.site.register(Author)
admin.site.register(Publisher)
