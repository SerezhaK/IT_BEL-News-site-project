from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.request import HttpRequest
from rest_framework.response import Response

from ..models.author import Author
from ..models.follow import Follow
from ..serializers.follow import FollowSerializer
from ..serializers.users import UserListSerializer


class FollowMixin:
    @extend_schema(tags=['follows'])
    @action(
        methods=['POST', ],
        detail=True,
        url_path='follow',
    )
    def follow(self, request: HttpRequest, pk: int):
        self.serializer_class = FollowSerializer
        author = get_object_or_404(Author, author_id=pk)
        data = {
            'author': author.author_id,
            'follower': self.request.user.user_id,
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'CREATED'}, status=201)

    @extend_schema(tags=['follows'])
    @action(
        methods=['POST', ],
        detail=True,
        url_path='unfollow',
    )
    def unfollow(self, request: HttpRequest, pk: int):
        author = get_object_or_404(Author, author_id=pk)
        follow = Follow.objects.filter(
            follower=self.request.user,
            author=author
        )
        follow.delete()
        return Response({'detail': 'NO_CONTENT'}, status=204)

    @extend_schema(tags=['follows'])
    @action(
        methods=['GET', ],
        detail=True,
        url_path='followers',
    )
    def author_follower_list(self, request: HttpRequest, pk: int):
        self.serializer_class = UserListSerializer
        get_object_or_404(Author, author_id=pk)
        followers = [i.follower for i in Follow.objects.filter(author=pk)]
        serializer = self.get_serializer(followers, many=True)
        return Response(serializer.data)
