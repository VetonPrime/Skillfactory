from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

article = 'AR'
news = 'NE'

CONTENTS = [
    (article, 'статья'),
    (news, 'новость')
]


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def update_rating(self):
        rating = 0
        # суммарный рейтинг каждой статьи автора умножается на 3;
        post_list = Post.objects.filter(author=self)
        for el_post in post_list:
            rating += el_post.rating * 3

            # суммарный рейтинг всех комментариев к статьям автора.
            post_comment_list = Comment.objects.filter(post=el_post)
            for el_post_comment in post_comment_list:
                rating += el_post_comment.rating

        # суммарный рейтинг всех комментариев автора;
        comment_list = Comment.objects.filter(user=self.user)
        for el_comment in comment_list:
            rating += el_comment.rating

        self.rating = rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.CharField(max_length=2, choices=CONTENTS, default=article)
    date_create = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    heading = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]}...'

    def get_absolute_url(self):
        return reverse('new_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    date_create = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
