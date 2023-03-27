from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .models import Post
from .filters import NewsFilter
from .forms import NewForm


class NewsList(ListView):
    model = Post
    ordering = '-date_create'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10


class NewsListSearch(NewsList):
    ordering = '-date_create'
    template_name = 'news_search.html'
    context_object_name = 'news_search'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class NewCreate(CreateView):
    form_class = NewForm
    model = Post
    template_name = 'new_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.content = 'NE'
        return super().form_valid(form)


class NewEdit(UpdateView):
    form_class = NewForm
    model = Post
    template_name = 'new_edit.html'


class NewDelete(DeleteView):
    model = Post
    template_name = 'new_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleCreate(CreateView):
    form_class = NewForm
    model = Post
    template_name = 'new_edit.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.content = 'AR'
        return super().form_valid(form)


class ArticleEdit(UpdateView):
    form_class = NewForm
    model = Post
    template_name = 'new_edit.html'


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'new_delete.html'
    success_url = reverse_lazy('news_list')
