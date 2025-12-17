from django.urls import path

from .views import (
    AddCommentView,
    CategoryPostsView,
    DeleteCommentView,
    EditCommentView,
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostUpdateView,
    ProfileView,
)

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path(
        'posts/<int:post_id>/',
        PostDetailView.as_view(),
        name='post_detail',
    ),
    path("posts/create/", PostCreateView.as_view(), name="create_post"),
    path(
        'posts/<int:post_id>/edit/',
        PostUpdateView.as_view(),
        name='post_edit',
    ),
    path(
        'posts/<int:post_id>/delete/',
        PostDeleteView.as_view(),
        name='post_delete',
    ),
    path(
        'profile/<str:username>/',
        ProfileView.as_view(),
        name='profile',
    ),
    path(
        'category/<slug:category_slug>/',
        CategoryPostsView.as_view(),
        name='category_posts',
    ),
    path(
        'posts/<int:post_id>/comment/',
        AddCommentView.as_view(),
        name='add_comment',
    ),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        EditCommentView.as_view(),
        name='edit_comment',
    ),
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        DeleteCommentView.as_view(),
        name='delete_comment',
    ),
]
