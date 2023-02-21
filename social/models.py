from django.db import models
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL

class Profile(models.Model):
    # Handle: blocked status, private account 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # private_account = models.BooleanField(default = False)
    name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='social/profile/images', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    following = models.ManyToManyField('self', blank=True, related_name='followers', symmetrical=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user.username}'

    def username(self) -> str:
        return str(self.user.username)


class Post(models.Model):
    # Handle: video content, geo-location, repost, likes, comments 
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content  = models.TextField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.content)

    class Meta:
        ordering = ['-created_at']


class PostImage(models.Model):
    post  = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='social/posts/images')


class PostLike(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    created_at  = models.DateTimeField(auto_now_add=True)


class PostComment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    is_flagged = models.BooleanField(null=True, blank=True, default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    