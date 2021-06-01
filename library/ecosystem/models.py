from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse

class Author(models.Model):

    salutation = models.CharField(_("Salutation"), choices=(('Mr.','Mr.'),('Ms.','Ms.'),('Mrs.','Mrs.')), default="Mr.", max_length=50)
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    date_of_birth = models.DateField(_("Date of Birth"), help_text="YYYY-MM-DD or MM/DD/YYYY")

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")

    def __str__(self):
        return self.salutation + " " + self.first_name + " " + self.last_name

    def get_absolute_url(self):
        return reverse("author_detail", kwargs={"pk": self.pk})

class Publisher(models.Model):

    name = models.CharField(_("Name"), max_length=50)
    address = models.TextField(_("Address"))
    city = models.CharField(_("City"), max_length=50)
    country = models.CharField(_("Country"), max_length=50)

    class Meta:
        verbose_name = _("Publisher")
        verbose_name_plural = _("Publishers")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("publisher_detail", kwargs={"pk": self.pk})
    
    def get_authors_worked_with(self):
        books = Book.objects.filter(publisher=self)
        author_set = set()
        for book in books:
            author_set.update(book.authors.all())
        return len(author_set)

class Book(models.Model):

    isbn_no = models.BigIntegerField(_("ISBN Number"), unique=True)
    name = models.CharField(_("Name"), max_length=50)
    preface = models.TextField(_("Preface"))
    summary = models.TextField(_("Summary"))
    pub_date = models.DateField(_("Publication Date (If published)"), help_text="YYYY-MM-DD or MM/DD/YYYY", blank=True, null=True)
    publisher = models.ForeignKey(Publisher, verbose_name=_("Publisher"), related_name=_("books"), on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author, verbose_name=_("Authors"), related_name=_("books"))

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"pk": self.pk})
