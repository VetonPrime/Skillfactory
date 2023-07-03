from django.db import models


class User(models.Model):
    """
    Класс модели для пользователей. Поля модели:
    email - уникальный адрес электронной почты;
    otc - отчество;
    phone - номер телефона.
    """
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=12)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.last_name}'

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'


class Coords(models.Model):
    """
    Класс модели для координат перевала.
    Поля модели:
    latitude - географическая широта;
    longitude - географическая долгота;
    height - высота над уровнем моря
    """
    latitude = models.FloatField(blank=True, null=True)
    longtitude = models.FloatField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "Координаты"
        verbose_name_plural = "Координаты"


class Level(models.Model):
    winter = models.TextField(blank=True, null=True)
    summer = models.TextField(blank=True, null=True)
    autumn = models.TextField(blank=True, null=True)
    spring = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Уровень сложности"
        verbose_name_plural = "Уровень сложности"


class Image(models.Model):
    """
    Класс модели для загружаемых картинок(фотографий перевалов):
    Поля модели:
    title - Название фотографии;
    image - фото перевала (в виде необработанных двоичных данных);
    date_added - время добавления фото.
    pereval - перевал, который сфотографировали (связан с моделью PerevalAdd);
    """
    title = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    image = models.ImageField(upload_to='media/', null=True, blank=True)

    def __str__(self):
        return f"title:{self.title}"

    class Meta:
        verbose_name = "Изображения"
        verbose_name_plural = "Изображения"


class Pereval(models.Model):
    STATUS_CHOICES = [
        ("new", "новый"),
        ("pending", "на рассмотрении"),
        ("accepted", "принят"),
        ("rejected", "отклонен"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coord = models.ForeignKey(Coords, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    images = models.ForeignKey(Image, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    beauty_title = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    other_titles = models.TextField(blank=True, null=True)
    connect = models.TextField(blank=True, null=True)
    add_time = models.TimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = "Перевал"
        verbose_name_plural = "Перевал"
