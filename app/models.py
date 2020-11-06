from django.db import models


class Users(models.Model):
    """Модель с данными пользователей. Есть поля с именем пользователя и
    паролем, которые используются для входа в личный кабинет пользователя.
    Поле token хранит код доступа пользователя при авторизации в личном
    кабинете."""

    name = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    token = models.UUIDField(null=True)


class Docs(models.Model):
    """Модель с документами пользователей."""

    user = models.ForeignKey(Users, on_delete=models.CASCADE)  # внешний ключ
    # на пользователя, загрузившего документ
    filepath = models.FilePathField()  # путь к файлу на сервере
    date = models.DateTimeField(auto_now=True)  # дата загрузки документа
    size = models.IntegerField()  # размер документа
    rating = models.IntegerField(default=0)  # рейтинг документа
    access = models.BooleanField(default=False)  # если True, документ доступен
    description = models.CharField(max_length=300, null=True)  # описание


class Ratings(models.Model):
    """Модель с данными о том, какой пользователь поставил рейтинг
    документу."""

    # Внешний ключ на документ
    doc = models.ForeignKey(Docs, on_delete=models.CASCADE)
    # Внешний ключ на пользователя, поставившего рейтинг документу
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    # Рейтинг, который поставил пользователь: -1 или +1
    rating = models.SmallIntegerField()
