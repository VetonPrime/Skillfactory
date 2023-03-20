from news.models import *

# Создать двух пользователей (с помощью метода User.objects.create_user('username')).
User.objects.create_user('Иванов')
User.objects.create_user('Петров')
User.objects.create_user('Сидоров')

# Создать два объекта модели Author, связанные с пользователями.
user1 = User.objects.all()[0]
user2 = User.objects.all()[1]

Author.objects.create(user=user1)
Author.objects.create(user=user2)

# Добавить 4 категории в модель Category.
Category.objects.create(name='Политика')
Category.objects.create(name='Спорт')
Category.objects.create(name='Авто')
Category.objects.create(name='Наука')

# Добавить 2 статьи и 1 новость.
Post1 = Post.objects.create(author=Author.objects.get(pk=1),
                            content=article,
                            heading='Про политику',
                            text='Тут будет текст статьи про политику. ' * 10)
Post2 = Post.objects.create(author=Author.objects.get(pk=1),
                            content=news,
                            heading='О спорте',
                            text='Тут будет текст статьи о спорте. ' * 10)
Post3 = Post.objects.create(author=Author.objects.get(pk=2),
                            content=article,
                            heading='Про машины',
                            text='Тут будет текст статьи про машины. ' * 10)

# Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
Post1.category.add(Category.objects.get(pk=1))
Post1.category.add(Category.objects.get(pk=2))
Post.objects.get(pk=2).category.add(Category.objects.get(pk=2))
Post.objects.get(pk=2).category.add(Category.objects.get(pk=3))
Post.objects.get(pk=3).category.add(Category.objects.get(pk=3))
Post.objects.get(pk=3).category.add(Category.objects.get(pk=4))
Post.objects.get(pk=3).category.add(Category.objects.get(pk=1))

# Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
Comment.objects.create(post=Post.objects.get(pk=1),
                       user=User.objects.all()[2],
                       text='Не интересная статья')
Comment.objects.create(post=Post.objects.get(pk=2),
                       user=User.objects.all()[1],
                       text='Отличная новость!!! Я очень рад!!')
Comment.objects.create(post=Post.objects.get(pk=2),
                       user=User.objects.all()[2],
                       text='Зенит чемпион!!!')
Comment.objects.create(post=Post.objects.get(pk=3),
                       user=User.objects.all()[0],
                       text='А у меня машина лучше.')
Comment.objects.create(post=Post.objects.get(pk=3),
                       user=User.objects.all()[1],
                       text='Продам зимнюю резину.')

# Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
Post.objects.get(pk=1).dislike()
Post.objects.get(pk=2).like()
Post.objects.get(pk=2).like()
Comment.objects.get(pk=2).like()
Comment.objects.get(pk=3).like()
Comment.objects.get(pk=3).like()
Comment.objects.get(pk=3).like()
Comment.objects.get(pk=4).dislike()
Comment.objects.get(pk=4).dislike()

# Обновить рейтинги пользователей.
author1 = Author.objects.get(pk=1)
author1.update_rating()
Author.objects.get(pk=2).update_rating()

# Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
top_author = Author.objects.all().order_by('-rating').values('user__username', 'rating')[0]
f'Лучший пользователь! username: {top_author["user__username"]}, рейтинг: {top_author["rating"]}'

# Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
top_post = Post.objects.filter(content=article).order_by('-rating').values('id', 'date_create', 'author__user__username', 'rating', 'heading')[0]
date_create = top_post["date_create"].strftime("%Y-%m-%d %H:%M:%S")
username = top_post["author__user__username"]
rating = top_post["rating"]
heading = top_post["heading"]
preview = Post.objects.get(pk=top_post["id"]).preview()
f'Лучшая статья! Дата добавления: {date_create}, username автора: {username}, рейтинг:{rating}, заголовок: "{heading}", превью: "{preview}"'

# Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
comment_list = Comment.objects.filter(post=Post.objects.get(pk=top_post["id"])).values('date_create', 'user__username', 'rating', 'text')
[[el['date_create'].strftime("%Y-%m-%d %H:%M:%S"), el['user__username'], el['rating'], el['text']] for el in comment_list]
