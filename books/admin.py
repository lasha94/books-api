from django.contrib import admin

from books.models import Book, Review


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "user", "status", "is_public")
    list_display_links = ("id", "title")
    list_filter = ("status", "is_public")
    search_fields = ("title", "author", "user__email")
    list_select_related = ("user",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "book", "user", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("book__title", "user__email", "comment")
    readonly_fields = ("created_at",)
    list_select_related = ("book", "user")