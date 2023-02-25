from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins , status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.exceptions import ValidationError
from social.permissions import IsAdminOrCurrentProfile, IsAdminOrReadOnly
from . import serializers, models

# Create your views here.
class ProfileViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'delete']
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAdminOrReadOnly]


    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def details(self, request):
        profile = models.Profile.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = serializers.ProfileSerializer(profile)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = serializers.ProfileSerializer(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class ProfileActionViewSet(mixins.CreateModelMixin,GenericViewSet):
    serializer_class = serializers.ProfileFollowActionSerializer
    queryset = models.Profile.objects.all()


    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def follow(self, request, pk=None):
        profile = self.get_object()
        user = request.user.profile
        if profile not in user.following.all():
            user.following.add(profile)
            user.save()
            return Response({'message':'Followed successfully'})
        else:
            return Response({'message':'Already following'})


    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk=None):
        profile = self.get_object()
        user = request.user.profile
        if profile in user.following.all():
            user.following.remove(profile)
            user.save()
            return Response({'message':'Unfollowed successfully'})
        else:
            return Response({'message':'Not following'})

                
class ProfileFollowListViewSet(mixins.ListModelMixin,GenericViewSet):
    serializer_class = serializers.ProfileFollowingListSerializer

    def get_queryset(self):
        return models.Profile.objects.filter(pk=self.kwargs['profile_pk'])

    def get_serializer_context(self):
        return {'profile_id': int(self.kwargs['profile_pk'])}


class PostViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = models.Post.objects\
        .select_related('profile')\
        .prefetch_related('post_likes')\
        .prefetch_related('files')\
        .all()
    serializer_class = serializers.PostSerializer
    filterset_fields = ['profile_id']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminOrCurrentProfile()]
        return [IsAuthenticatedOrReadOnly()]


    def get_serializer_context(self):
        return {'user_id': self.request.user.id}



class PostLikeViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    serializer_class = serializers.PostLikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return models.PostLike.objects.filter(post_id=self.kwargs['post_pk'])

    def get_serializer_context(self):
        return {
            'post_id': self.kwargs['post_pk'],
            'user_id': self.request.user.id
            }    


class PostCommentViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    serializer_class = serializers.PostCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return models.PostComment.objects.filter(post_id=self.kwargs['post_pk'])

    def get_serializer_context(self):
        return {
            'post_id': self.kwargs['post_pk'],
            'user_id': self.request.user.id
            }    


class CommentReplyViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['comment_id']
    http_method_names = ['get', 'post', 'delete']
    queryset = models.CommentReply.objects.all()
    def get_serializer_context(self):
        return {
            'user_id': self.request.user.id
            }  
    
    def get_queryset(self):
        comment_id = self.request.query_params.get('comment_id')
        if not comment_id:
            raise ValidationError({'comment_id': 'This field is required.'})
        queryset = super().get_queryset()
        queryset = queryset.filter(comment_id=comment_id)
        return queryset


    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ListCommentReply
        return serializers.CommentReplySerializer
        