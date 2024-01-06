from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from .cloths import Cloth
from accounts.models import User

class ActiveCommentsManager(models.Manager):
    def get_queryset(self):
        return super(ActiveCommentsManager, self).get_queryset().filter(active=True)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')
    cloth = models.ForeignKey(Cloth, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(verbose_name=_('please write your opinion here'))
    active = models.BooleanField(default=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.cloth}: {self.body}'

    # manager
    objects = models.Manager()
    active_comments_manager = ActiveCommentsManager()

    # def get_absolute_url(self):
    #     return reverse('cloth_detail', args=[self.cloth.id])