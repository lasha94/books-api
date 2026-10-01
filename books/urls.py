from django.urls import path

from books.views import (
    BookDetailView,
    BookListCreateView,
    PublicBookDetailView,
    PublicBookListView,
    ReviewDetailView,
    ReviewListCreateView,
)

app_name = "books"

urlpatterns = [
    path(
        "",
        BookListCreateView.as_view(),
        name="book-list",
    ),
    path(
        "<int:book_id>/",
        BookDetailView.as_view(),
        name="book-detail",
    ),
    path(
        "public/",
        PublicBookListView.as_view(),
        name="public-book-list",
    ),
    path(
        "public/<int:book_id>/",
        PublicBookDetailView.as_view(),
        name="public-book-detail",
    ),
    path(
        "public/<int:book_id>/reviews/",
        ReviewListCreateView.as_view(),
        name="review-list",
    ),
    path(
        "reviews/<int:pk>/",
        ReviewDetailView.as_view(),
        name="review-detail",
    ),
]