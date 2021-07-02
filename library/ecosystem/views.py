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



#############################################################################################

from django.forms.models import inlineformset_factory
from django.urls import reverse

class ParentCreateView(CreateView):
    model = Publisher
    fields = ('name', 'address', 'city', 'country')
    template_name = 'ecosystem/inline_formset.html'

    def get_context_data(self, **kwargs):
        # we need to overwrite get_context_data
        # to make sure that our formset is rendered
        ChildFormset = inlineformset_factory(
            Publisher, Book, fields=('isbn_no', 'name', 'preface', 'summary', 'pub_date', 'authors')
        )
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["children"] = ChildFormset(self.request.POST)
        else:
            data["children"] = ChildFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        children = context["children"]
        self.object = form.save()
        if children.is_valid():
            children.instance = self.object
            children.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("publisher_list")

class ParentUpdateView(UpdateView):
    model = Publisher
    fields = ('name', 'address', 'city', 'country')
    template_name = 'ecosystem/inline_formset.html'

    def get_context_data(self, **kwargs):
        # we need to overwrite get_context_data
        # to make sure that our formset is rendered.
        # the difference with CreateView is that
        # on this view we pass instance argument
        # to the formset because we already have
        # the instance created
        ChildFormset = inlineformset_factory(
            Publisher, Book, fields=('isbn_no', 'name', 'preface', 'summary', 'pub_date', 'authors'), 
        )
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["children"] = ChildFormset(self.request.POST, instance=self.object)
        else:
            data["children"] = ChildFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        children = context["children"]
        self.object = form.save()
        if children.is_valid():
            children.instance = self.object
            children.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("publisher_list")
