from datetime import datetime
from django.views.generic import ListView, DetailView
from .models import News


class NewsList(ListView):
    model = News
    ordering = 'Title'
    template_name = 'news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class NewsDetail(DetailView):
    model = News
    template_name = 'news_item.html'
    context_object_name = 'news_item'
