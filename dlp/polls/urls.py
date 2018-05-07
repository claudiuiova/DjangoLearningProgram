from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.pollview, name='pollview'),
    path('<int:poll_id>/page/<int:page_idx>', views.pages, name='pages'),
    path('result/poll/<int:poll_id>', views.result, name='result'),
]
