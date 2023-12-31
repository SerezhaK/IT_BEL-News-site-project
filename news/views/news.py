from rest_framework import filters, viewsets
from rest_framework.exceptions import ValidationError

from ..mixins.like import DislikeMixin, LikeMixin
from ..models.news import News
from ..permissions.news import AuthorOrReadOnlyNews
from ..serializers.news import NewsSerializer
from news.mixins.news import NewsMixin
from users.models.user import User


class NewsViewSet(LikeMixin,
                  DislikeMixin,
                  NewsMixin,
                  viewsets.ModelViewSet):

    queryset = News.objects.prefetch_related(
        'votes', 'tags'
    ).select_related(
        'author'
    )
    serializer_class = NewsSerializer
    permission_classes = [AuthorOrReadOnlyNews]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def perform_create(self, serializer: NewsSerializer):
        user: User = self.request.user
        if not hasattr(user, 'author'):
            raise ValidationError({'detail': 'Only authors can create News'})
        return serializer.save(author=user.author)
