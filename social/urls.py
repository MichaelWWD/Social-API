from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()


router.register('profiles', views.ProfileViewSet, basename='social-profiles')
router.register('profiles/actions', views.ProfileActionViewSet, basename='profile-actions')

profiles_router = routers.NestedDefaultRouter(router, 'profiles', lookup='profile')
profiles_router.register('followings', views.ProfileFollowListViewSet,basename='profile-following')


router.register('posts', views.PostViewSet, basename='social-posts')
posts_router = routers.NestedDefaultRouter(router, 'posts', lookup='post')
posts_router.register('likes', views.PostLikeViewSet, basename='post-likes')
posts_router.register('comments', views.PostCommentViewSet, basename='post-comments')


# URLConf
urlpatterns = router.urls + profiles_router.urls + posts_router.urls

