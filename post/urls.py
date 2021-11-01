from django.urls import path

from post import views

app_name = 'post'

urlpatterns = [
    path('', views.list_post_view, name='list-post'),
    path('like/', views.like_unlike_post_view, name='like-unlike'),
    path('create/post/', views.create_post_view, name='create-post'),
    path('create/comment/', views.create_comment_view, name='create-comment'),

    path('delete/<int:pk>/', views.DeletePostView.as_view(), name='delete-post'),
    path('update/<int:pk>/', views.UpdatePostView.as_view(), name='update-post'),
]
