from django.urls import path
from .views import NewsList, NewsDetail, NewsCreate, NewsUpdate, NewsDelete, CreateSubscribeView, UnSubscribeView


urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('sign/subscribe/', CreateSubscribeView.as_view(template_name='subscribe.html'), name='subscription'),
    path('sign/<int:pk>/unsubscribe', UnSubscribeView.as_view(), name='unsubscribe'),
]
