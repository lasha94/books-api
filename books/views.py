from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import Book, Review
from books.serializers import BookSerializer, ReviewSerializer


@extend_schema(tags=["Books"])
class BookListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="ჩემი წიგნები",
        responses={200: BookSerializer(many=True)},
    )
    def get(self, request):
        books = Book.objects.filter(
            user=request.user,
        ).order_by("-id")

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="წიგნის დამატება",
        request=BookSerializer,
        responses={
            201: BookSerializer,
            400: OpenApiResponse(description="არასწორი მონაცემები."),
        },
    )
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


@extend_schema(tags=["Books"])
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "book_id"

    def get_queryset(self):
        return Book.objects.filter(user_id=self.request.user.id)


@extend_schema(
    tags=["Public Books"],
    summary="საჯარო წიგნების სია",
)
class PublicBookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.filter(is_public=True).order_by("-id")


@extend_schema(
    tags=["Public Books"],
    summary="საჯარო წიგნის ნახვა",
)
class PublicBookDetailView(generics.RetrieveAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "book_id"
    queryset = Book.objects.filter(is_public=True)


@extend_schema(tags=["Reviews"], summary="წიგნის შეფასებები")
class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(
            book_id=self.kwargs.get("book_id"),
            book__is_public=True,
        )

    def perform_create(self, serializer):
        book = Book.objects.filter(
            id=self.kwargs["book_id"],
            is_public=True,
        ).first()

        if book is None:
            raise NotFound("წიგნი ვერ მოიძებნა.")

        serializer.save(
            user=self.request.user,
            book=book,
        )


@extend_schema(tags=["Reviews"])
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(
            user_id=self.request.user.pk,
            book__is_public=True,
        )