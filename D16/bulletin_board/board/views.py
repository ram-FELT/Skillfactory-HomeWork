from django.http import request, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import *
from django.urls import reverse_lazy
from .apscheduler import go_mail

class RegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/activate'

    def form_valid(self, form):
        form.instance.is_active = False
        self.request.session['activation_state'] = ''
        return super(RegisterView, self).form_valid(form)


class ActivateView(View):
    template_name = 'activate.html'

    def post(self, request):
        email = request.POST.get('email')
        otc_code = request.POST.get('otc')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            author = Author.objects.get(author=user)
            if author.otc[:6] == otc_code:
                if int(author.otc[-10:]) + 3600 > datetime.timestamp(datetime.now()):
                    user.is_active = True
                    user.save()
                    request.session['activation_state'] = 'success'
                else:
                    author.delete()
                    user.delete()
                    request.session['activation_state'] = 'reregister'
            else:
                request.session['activation_state'] = 'reenter_code'
        else:
            request.session['activation_state'] = 'reenter_email'
        return redirect('/activate/')

    def get(self, request):
        return render(request, 'activate.html')


class IndexView(LoginRequiredMixin, TemplateView):
    def post(self, request):
        if request.POST['mail'] == 'do_it':
            go_mail.send_robust(sender='Weekly')
        return redirect('/')


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = Author.objects.get(author=self.request.user)
        return super(PostCreate, self).form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'editpost.html'


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


class PostList(ListView):
    model = Post
    ordering = '-creation_date'
    context_object_name = 'posts'
    paginate_by = 20


class PostView(DetailView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Post.objects.get(id=self.request.path.split('/')[-1]).comments.all()
        return context

    def post(self, request, *args, **kwargs):
        for i in Comment.objects.all():
            comment_choice = request.POST.get(str(i.pk))
            print(comment_choice, ' comment ', i.pk)
            if comment_choice == 'accept':
                i.accepted = True
                i.save()
            elif comment_choice == 'delete':
                i.delete()
        return HttpResponseRedirect(request.path)


class CommentCreate(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    model = Comment
    template = 'comment_create.html'

    def form_valid(self, form):
        form.instance.post = Post.objects.get(id=self.request.path.split('/')[-2])
        form.instance.commentator = self.request.user
        return super(CommentCreate, self).form_valid(form)

    def get_success_url(self):
        return self.request.path[:-8]


class CommentsManageView(LoginRequiredMixin, ListView):
    model = Comment
    context_object_name = 'comments'
    paginate_by = 20

    def get_queryset(self):
        return Comment.objects.filter(post__in=Post.objects.filter(author=Author.objects.get(author=self.request.user))).order_by('-creation_date')
