from rest_framework import serializers

from books.models import Book, Review


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "status",
            "is_public",
            "user",
        )
        read_only_fields = ("id", "user")


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "id",
            "book",
            "user",
            "rating",
            "comment",
            "created_at",
        )
        read_only_fields = ("id", "book", "user", "created_at")