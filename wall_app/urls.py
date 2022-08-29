from django.urls import path
from wall_app.views import PostViewSet, CommentCreateViewSet, LikeView


urlpatterns = [
    path('', PostViewSet.as_view({'get': 'list', 'post': 'create'}), name='posts'),
    path('<int:pk>', PostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('<int:post_pk>/comment/create', CommentCreateViewSet.as_view({'post': 'create'})),
    path('<int:post_pk>/like/', LikeView.as_view()),
]

