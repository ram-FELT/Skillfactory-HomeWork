from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .filters import NewsFilter
from .forms import NewsForm
from .models import News


class NewsList(ListView):
    model = News
    ordering = 'Title'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 5

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = News
    template_name = 'news_item.html'
    context_object_name = 'news_item'


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_news',)
    form_class = NewsForm
    model = News
    template_name = 'news_edit.html'


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_news',)
    form_class = NewsForm
    model = News
    template_name = 'news_edit.html'


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_news',)
    model = News
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')

