from django.urls import path
from .views import *

urlpatterns = [
    path('post_create', PostCreate.as_view(template_name='post_create.html'), name='post_create'),
    path('<int:pk>', PostView.as_view(template_name='post_detail.html'), name='post_detail'),
    path('<int:pk>/edit', PostUpdate.as_view(template_name='post_update.html'), name='post_update'),
    path('<int:pk>/delete', PostDelete.as_view(template_name='post_delete.html'), name='post_delete'),
    path('<int:pk>/comment', CommentCreate.as_view(template_name='comment_create.html'), name='comment'),
    path('post_list', PostList.as_view(template_name='post_list.html'), name='post_list'),
    path('my_comments', CommentsManageView.as_view(template_name='my_comments.html'), name='my_comments'),
    ]
