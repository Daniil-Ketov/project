# coding=utf-8
from audioop import reverse
from django.contrib.auth.models import User
from django.db import models


GENDER_CHOICES = [
    ['male', u"Мужской"],
    ['female', u"Женский"],
    ['secret', u"Секрет"]
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=u"Пользователь")
    avatar = models.FileField(verbose_name=u"Аватар", null=True, blank=True)
    bio = models.TextField(max_length=1000, blank=True, null=True, verbose_name=u"О себе")
    city = models.CharField(max_length=40, blank=True, null=True, verbose_name=u"Город")
    birth_date = models.DateField(null=True, blank=True, verbose_name=u"Дата рождения")
    gender = models.CharField(max_length=10, verbose_name=u"Пол", choices=GENDER_CHOICES, default="male")
    

class Post(models.Model):
    datetime = models.DateTimeField(verbose_name=u"Дата", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=u"Автор", related_name="posts")
    text = models.CharField(max_length=1000, verbose_name=u"Текст", null=True, blank=True)
    image = models.FileField(verbose_name=u"Картинка", null=True, blank=True)

    class Meta:
        ordering = ["-datetime"]
        

class Comment(models.Model):
    datetime = models.DateTimeField(verbose_name=u"Дата", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=u"Автор", related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=u"Пост", related_name="comments")
    text = models.CharField(max_length=1000, verbose_name=u"Текст", null=True, blank=True)

    class Meta:
        ordering = ["datetime"]
        

class Friends(models.Model):
    users1=models.ManyToManyField(User)
    current_user=models.ForeignKey(User, related_name='Владелец', on_delete=models.CASCADE, null=True)


    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend,create=cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users1.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, create = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users1.remove(new_friend)


class FriendRequest(models.Model):
    sender=models.ForeignKey(User, null=True, related_name='Отправитель', on_delete=models.CASCADE)
    receiver=models.ForeignKey(User, null=True, related_name='Получатель', on_delete=models.CASCADE)


class Chat(models.Model):
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, 'Dialog'),
        (CHAT, 'Chat')
    )
 
    type = models.CharField(
        max_length=1,
        choices=CHAT_TYPE_CHOICES,
        default='D'
    )
    members = models.ManyToManyField(User, verbose_name=u"Участник")
 
    def get_absolute_url(self):
        return reverse('users:messages', args=((), {'chat_id': self.pk }))
 
 
class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name=u"Чат", on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name=u"Пользователь", on_delete=models.CASCADE)
    message = models.TextField(max_length=1000, verbose_name=u"Сообщение", null=True, blank=True)
    pub_date = models.DateTimeField(verbose_name=u"Дата сообщения", auto_now_add=True)
    is_readed = models.BooleanField(verbose_name=u"Прочитано", default=False)
 
    class Meta:
        ordering=['pub_date']
 
    def __str__(self):
        return self.message
    
