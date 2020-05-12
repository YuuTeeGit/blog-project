from django.urls import path
from django.conf.urls import url
from blog import views

urlpatterns = [
    path('',views.PostListView.as_view(),name='post_list'),
    path('about/',views.AboutView.as_view(),name='about'),
    url(r'^post/(?P)<pk>\d+)$',views.PostDetailView.as_view(),name='post_detail'),
    path('post/new/',views.CreatePostView.as_view(),name='post_new'),
    url(r'^post/(?P)<pk>\d+)/edit/$',views.UpdateView.as_view(),name='post_update'),
    url(r'^post/(?P)<pk>\d+)/remove/$',views.DeleteView.as_view(),name='post_remove'),
    path('drafts/',views.DraftListView.as_view(),name='post_draft_list'),
]