from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.db.models import Count, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Author, Publisher, Book


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "ecosystem/home.html"



# AUTHOR CBV

class AuthorListView(LoginRequiredMixin, ListView):
    queryset = Author.objects.all().annotate(count=Count('books', filter=Q(books__pub_date__isnull=False)))

class AuthorDetailView(LoginRequiredMixin, DetailView):
    queryset = Author.objects.all().prefetch_related('books').annotate(
        published=Count('books', filter=Q(books__pub_date__isnull=False)),
        draft=Count('books', filter=Q(books__pub_date__isnull=True))
    )

class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = Author
    fields = ('salutation', 'first_name', 'last_name', 'date_of_birth')

class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    model = Author
    fields = ('salutation', 'first_name', 'last_name', 'date_of_birth')



# PUBLISHER CBV

class PublisherListView(LoginRequiredMixin, ListView):
    queryset = Publisher.objects.all().only('name').annotate(count=Count('books', filter=Q(books__pub_date__isnull=False)))

class PublisherDetailView(LoginRequiredMixin, DetailView):
    queryset = Publisher.objects.all().prefetch_related('books').all().annotate(
        published=Count('books', filter=Q(books__pub_date__isnull=False)),
        draft=Count('books', filter=Q(books__pub_date__isnull=True))
    )

class PublisherCreateView(LoginRequiredMixin, CreateView):
    model = Publisher
    fields = ('name', 'address', 'city', 'country')

class PublisherUpdateView(LoginRequiredMixin, UpdateView):
    model = Publisher
    fields = ('name', 'address', 'city', 'country')



# BOOK CBV

class BookListView(LoginRequiredMixin, ListView):
    model = Book

class BookDetailView(LoginRequiredMixin, DetailView):
    queryset = Book.objects.select_related('publisher').prefetch_related('authors').all()

class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    fields = ('isbn_no', 'name', 'preface', 'summary', 'pub_date', 'publisher', 'authors')

class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ('isbn_no', 'name', 'preface', 'summary', 'pub_date', 'publisher', 'authors')

class BookPublishView(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ('pub_date',)
    template_name = 'ecosystem/book_publish.html'