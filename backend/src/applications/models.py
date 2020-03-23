import uuid

from django.contrib.auth.models import User
from django.db import models
from project.models import BaseModel


class Application(BaseModel):
    owner = models.ForeignKey(
        User,
        'Владелец приложения',
        null=False,
        blank=False,
    )
    name = models.CharField(
        'Название приложения',
        max_length=200,
        null=False,
        blank=False,
        default=None,
    )
    api_key = models.UUIDField(
        'Ключ API',
        default=uuid.uuid4,
        unique=True
    )

    def refresh_key(self):
        self.api_key = uuid.uuid4()
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        '''
        Make sure the key is unique
        '''
        verbose_name = 'Приложение'
        verbose_name_plural = 'Приложения'
