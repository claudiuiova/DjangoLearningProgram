from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('polls/', views.pollview, name='pollview'),
    path('polls/<int:poll_id>/page/<int:page_idx>', views.pages, name='pages'),
    path('polls/poll<int:poll_id>/results', views.result, name='result'),
    path('statistics', views.statistics, name='statistics'),
    path('login', views.login_as_admin, name='adminlogin'),
    path('statistics/poll_attempts', views.poll_attempts, name='attempts'),
    path('statistics/polls', views.pollview_stats, name='pollviewstats'),
    path('statistics/polls/<int:poll_id>', views.statistics_results, name='statisticsresults'),
    path('statistics/polls/<int:poll_id>/user/<str:user>', views.user_result, name='userresult'),
    path('statistics/mwq/polls', views.most_wrong_questions_polls, name='mostwrongquestions'),
    path('statistics/mwq/polls/<int:poll_id>', views.most_wrong_questions_results, name='mostwrongquestionsresults')
]
