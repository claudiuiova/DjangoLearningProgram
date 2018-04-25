from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.pollview, name='pollview'),
    path('<int:poll_id>', views.pages, name='pages'),
    path('^/<int:page_id>', views.questions, name='questions'),
]