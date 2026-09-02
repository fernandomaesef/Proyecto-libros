from django.db import models
from django.conf import settings

# Create your models here.

class Book(models.Model):
    api_id = models.CharField(max_length=100,unique=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13,unique=True,null=True,blank=True)
    published_date = models.DateField(null=True,blank=True)
    cover_url = models.URLField(blank=True)

    def __str__(self):
        return self.title

class UserBook(models.Model):

    class Status(models.TextChoices):
        ADDED = "added","Added"
        READING ="reading","Reading"
        READ = "read","Read"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    rating = models.PositiveSmallIntegerField(null=True,blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ADDED
        )
    
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user","book"],
                name="unique_user_book"
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(rating__gte=1,rating__lte=5) 
                    | models.Q(rating__isnull=True)
                ),
                name="rating_between_1_and_5"
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(status__in=["added","reading","read"])
                ),
                name='status_restriction'
            )
        ]