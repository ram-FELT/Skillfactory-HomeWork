from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .filters import NewsFilter
from .forms import *
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
    permission_required = ('News.add_news',)
    form_class = NewsForm
    model = News
    template_name = 'news_edit.html'


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('News.change_news',)
    form_class = NewsForm
    model = News
    template_name = 'news_edit.html'


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('News.delete_news',)
    model = News
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class CreateSubscribeView(LoginRequiredMixin, CreateView):
    form_class = SubscribeForm
    model = Subscribe
    template_name = 'subscribe.html'
    success_url = reverse_lazy('subscription')

    def form_valid(self, form):
        form.instance.subscriber = User.objects.get(id=self.request.user.id)
        if Subscribe.objects.filter(category=form.instance.category, subscriber=form.instance.subscriber):
            return super(CreateSubscribeView, self).form_invalid(form)
        else:
            return super(CreateSubscribeView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mysubscribes'] = Subscribe.objects.filter(subscriber=User.objects.get(id=self.request.user.id))
        return context


class UnSubscribeView(LoginRequiredMixin, DeleteView):
    model = Subscribe
    template_name = 'unsubscribe.html'
    success_url = reverse_lazy('subscription')
