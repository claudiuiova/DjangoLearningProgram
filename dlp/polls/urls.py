from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('polls/', views.pollview, name='pollview'),
    path('polls/<int:poll_id>/page/<int:page_idx>', views.pages, name='pages'),
    path('polls/poll<int:poll_id>/results', views.result, name='result'),
    path('statistics', views.statistics, name='statistics'),
    path('statistics/poll_attempts', views.poll_attempts, name='attempts')
]
