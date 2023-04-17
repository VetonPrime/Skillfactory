from django.urls import path
from .views import (
   NewsList, NewDetail, NewsListSearch, NewCreate, NewEdit, NewDelete, ArticleCreate, ArticleEdit, ArticleDelete,
   BaseRegisterView, upgrade_me
)
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
   path('', NewsList.as_view(), name='news_list'),
   path('<int:pk>', NewDetail.as_view(), name='new_detail'),
   path('search/', NewsListSearch.as_view(), name='news_search'),
   path('new/create/', NewCreate.as_view(), name='new_create'),
   path('new/<int:pk>/edit/', NewEdit.as_view(), name='new_edit'),
   path('new/<int:pk>/delete/', NewDelete.as_view(), name='new_delete'),
   path('article/create/', ArticleCreate.as_view(), name='articles_create'),
   path('article/<int:pk>/edit/', ArticleEdit.as_view(), name='articles_edit'),
   path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='articles_delete'),
   path('login/',
        LoginView.as_view(template_name='news/login.html'),
        name='login'),
   path('logout/',
        LogoutView.as_view(template_name='news/logout.html'),
        name='logout'),
   path('signup/',
        BaseRegisterView.as_view(template_name='news/signup.html'),
        name='signup'),
   path('upgrade/', upgrade_me, name='upgrade'),
]
