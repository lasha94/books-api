from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class Book(models.Model):
    class Status(models.TextChoices):
        TO_READ = "to_read", "წასაკითხი"
        READING = "reading", "ვკითხულობ"
        FINISHED = "finished", "წაკითხული"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TO_READ,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="books",
    )
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} — {self.author}"

class Review(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    comment = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.book.title} — {self.rating}/5"