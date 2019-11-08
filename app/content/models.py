from django.db import models

from app.util.models import BaseModel, OptionalImage
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
from datetime import datetime, timezone, timedelta


class News(BaseModel, OptionalImage):
    title = models.CharField(max_length=200)
    header = models.CharField(max_length=200)
    body = models.TextField()

    class Meta:
        verbose_name_plural = 'News'

    def __str__(self):
        return '{} - {} [{} characters]'.format(self.title,
                                                self.header, len(self.body))


class Category(BaseModel):
    text = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.text}'


class Warning(BaseModel):
    text = models.CharField(max_length=400, null=True)
    TYPES = (
        (0, 'Error'),
        (1, 'Warning'),
        (2, 'Message'),
    )
    type = models.IntegerField(default=0, choices=TYPES, null=True)

    def __str__(self):
        return f'Warning: {self.type} - Text: {self.text}'


class JobPost(BaseModel, OptionalImage):
    title = models.CharField(max_length=200)
    ingress = models.CharField(max_length=800)
    body = models.TextField(blank=True, default='')
    location = models.CharField(max_length=200)

    deadline = models.DateTimeField(null=True, blank=True)

    company = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    link = models.URLField(max_length=300, blank=True, null=True)

    @property
    def expired(self):
        return self.deadline <= datetime.now(tz=timezone.utc)-timedelta(days=1)

    def __str__(self):
        return f'JobPost: {self.company}  - {self.title}'


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, user_id, password=None):
        user = self.model(
            user_id = user_id,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, user_id, password=None):
        user = self.create_user(
            user_id = user_id,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password):
        user = self.create_user(
            user_id = user_id,
            password = password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, BaseModel, OptionalImage):
    user_id = models.CharField(max_length=15, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    email = models.EmailField(max_length=254)
    cell = models.CharField(max_length=8, blank=True)

    em_nr = models.CharField(max_length=12, blank=True)
    home_busstop = models.IntegerField(null=True, blank=True)

    GENDER = (
        (1, 'Mann'),
        (2, 'Kvinne'),
        (3, 'Annet'),
    )
    gender = models.IntegerField(default=2, choices=GENDER, null=True, blank=True)
    CLASS = (
        (1, '1. Klasse'),
        (2, '2. Klasse'),
        (3, '3. Klasse'),
        (4, '4. Klasse'),
        (5, '5. Klasse'),
    )
    user_class = models.IntegerField(default=1, choices=CLASS, null=True, blank=True)

    STUDY = (
        (1, 'Dataing'),
        (2, 'DigFor'),
        (3, 'DigInc'),
        (4, 'DigSam'),
    )
    user_study = models.IntegerField(default=1, choices=STUDY, null=True, blank=True)
    allergy = models.CharField(max_length=250, blank=True)

    tool = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = 'user_id'
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'User - {self.user_id}: {self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    objects = UserManager()


class Event(BaseModel, OptionalImage):
    title = models.CharField(max_length=200)
    start = models.DateTimeField()
    location = models.CharField(max_length=200, null=True)
    description = models.TextField(default='', blank=True)

    PRIORITIES = (
        (0, 'Low'),
        (1, 'Normal'),
        (2, 'High'),
    )
    priority = models.IntegerField(default=0, choices=PRIORITIES, null=True)

    category = models.ForeignKey(Category, blank=True,
                                    null=True, default=None,
                                    on_delete=models.SET_NULL)

    sign_up = models.BooleanField(default=False)
    limit = models.IntegerField(default=0)
    closed = models.BooleanField(default=False)
    registered_users_list = models.ManyToManyField(User, through='UserEvent', through_fields=('event', 'user'), blank=True, default=None)

    @property
    def expired(self):
        return self.start <= datetime.now(tz=timezone.utc)-timedelta(days=1)

    def __str__(self):
        return f'{self.title} - starting {self.start} at {self.location}'


class UserEvent(BaseModel):
    """ Model for users registration for an event """
    user_event_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    is_on_wait = models.BooleanField(default=False)
    has_attended = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'event')
        verbose_name = "User event"
        verbose_name_plural = 'User events'
    
    def __str__(self):
        return f'{self.user.email} - is to attend {self.event} and is ' \
               f'{ "on the waitinglist" if self.is_on_wait else "on the list"}'
