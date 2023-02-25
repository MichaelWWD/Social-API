from rest_framework import serializers
from . import models


class SimpleProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = ['id','username','avatar']


class ProfileSerializer(serializers.ModelSerializer):
    follower_count = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.Profile
        fields = ['id', 'username','bio','avatar', 'follower_count', 'following_count']


    def get_following_count(self, profile) -> int:
        return profile.following.count()
    
    def get_follower_count(self, profile) -> int:
        return profile.followers.count()


class ProfileFollowActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = ['id', 'following']


class ProfileFollowingListSerializer(serializers.ModelSerializer):
    following = SimpleProfileSerializer(many=True, read_only=True)
    followers = SimpleProfileSerializer(many=True, read_only=True)
    class Meta:
        model = models.Profile
        fields = ['id', 'following', 'followers']


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PostImage
        fields = ['id','image']


class PostSerializer(serializers.ModelSerializer):
    profile = SimpleProfileSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    images = PostImageSerializer(many=True, required=False, read_only=True)
    uploaded_images = serializers.ListField(
        child = serializers.ImageField(max_length = 1000000, allow_empty_file = False, use_url = False), required=False, write_only=True)

    class Meta:
        model = models.Post
        fields = [
            'id', 'profile', 'content', 
            'images', 'uploaded_images', 
            'comments_count' ,'likes_count',
            'created_at', 'updated_at']
    
    
    def get_comments_count(self, posts) -> int:
        return posts.comments.count()

    def get_likes_count(self, posts) -> int:
        return posts.post_likes.count()

    def create(self, validated_data):
        profile = models.Profile.objects.get(user_id=self.context['user_id'])
        try: 
            uploaded_images = validated_data.pop("uploaded_images")
            post = models.Post.objects.create(profile_id=profile.id, **validated_data)
            for image in uploaded_images:
                post_image = models.PostImage.objects.create(post=post,image=image)
        except KeyError:
            post = models.Post.objects.create(profile_id=profile.id, **validated_data)
        return post


class PostLikeSerializer(serializers.ModelSerializer):
    profile = SimpleProfileSerializer(read_only=True)
    class Meta:
        model = models.PostComment
        fields = ['id', 'profile','created_at']


    def create(self, validated_data):
        profile = models.Profile.objects.get(user_id=self.context['user_id'])
        post_id = self.context['post_id']
        return models.PostLike.objects.create(profile_id=profile.id, post_id=post_id, **validated_data)



class PostCommentSerializer(serializers.ModelSerializer):
    profile = SimpleProfileSerializer(read_only=True)
    reply_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.PostComment
        fields = ['id', 'profile', 'text', 'reply_count','created_at']

    def get_reply_count(self, comments) -> int:
        return comments.replies.count()


    def create(self, validated_data):
        profile = models.Profile.objects.get(user_id=self.context['user_id'])
        post_id = self.context['post_id']
        return models.PostComment.objects.create(profile_id=profile.id, post_id=post_id, **validated_data)


class CommentReplySerializer(serializers.ModelSerializer):
    comment_id = serializers.IntegerField()

    class Meta:
        model = models.CommentReply
        fields = ['id', 'comment_id','text', 'created_at']

    def validate_comment_id(self, comment_id):
        if not models.PostComment.objects.filter(pk=comment_id).exists():
            raise serializers.ValidationError(
                'No comment with the given ID was found.')
        return comment_id


    def create(self, validated_data):
        profile = models.Profile.objects.get(user_id=self.context['user_id'])
        return models.CommentReply.objects.create(profile_id=profile.id, **validated_data)


class ListCommentReply(serializers.ModelSerializer):
    profile = SimpleProfileSerializer(read_only=True)

    class Meta:
        model = models.CommentReply
        fields = ['id', 'profile','text', 'comment_id', 'created_at']

    
