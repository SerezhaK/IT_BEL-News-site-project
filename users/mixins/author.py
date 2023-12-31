from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.request import HttpRequest
from rest_framework.response import Response

from ..models.author import Author
from news.serializers.news import NewsSerializer
from users.permissions.moderator import IsModerator


class AuthorMixin:
    @action(
        methods=['GET', ],
        detail=True,
        url_path='news',
    )
    def get_author_news(self, request: HttpRequest, pk: int):
        self.serializer_class = NewsSerializer
        author = get_object_or_404(Author, author_id=pk)
        news = author.news.all()
        serializer = self.get_serializer(news, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['GET', ],
        url_path='author_stats',
        permission_classes=[IsModerator, ]
    )
    def registration_counts(self, request: HttpRequest):
        today = timezone.now().date()
        week_start = today - timezone.timedelta(days=today.weekday())
        month_start = today.replace(day=1)

        today_count = self.queryset.filter(
            date_joined__gte=today
        ).count()
        week_count = self.queryset.filter(
            date_joined__gte=week_start
        ).count()
        month_count = self.queryset.filter(
            date_joined__gte=month_start
        ).count()

        data = {
            'today': today_count,
            'this_week': week_count,
            'this_month': month_count,
        }

        return Response(data)
