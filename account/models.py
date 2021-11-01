from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from django.utils.text import slugify

from account.utils import get_random_code
from account.manager import RelationshipManager, ProfileManager


class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="no bio...", max_length=300)
    email = models.EmailField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ProfileManager()

    def __str__(self):
        return f'{self.user.username}-{self.created.strftime("%d-%m-%Y")}'

    def get_absolute_url(self):
        return reverse('account:detail-profile', kwargs={'slug': self.slug})

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

    def get_posts(self):
        return self.posts.all()

    def get_posts_no(self):
        return self.posts.all().count()

    def get_likes_given_no(self):
        likes = self.user_likes.all()
        total_likes = 0

        for like in likes:
            if like.value == like.LIKE:
                total_likes += 1
        return total_likes

    def get_likes_received_no(self):
        total_likes = 0

        for post in self.get_posts():
            total_likes += post.liked.all().count()
        return total_likes

    __init_first_name = None
    __init_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__init_first_name = self.first_name
        self.__init_last_name = self.last_name

    def save(self, *args, **kwargs):
        to_slug = self.slug

        if self.first_name != self.__init_first_name or self.last_name != self.__init_last_name or self.slug == '':
            if self.first_name and self.last_name:
                to_slug = slugify(self.full_name)
                existing = Profile.objects.filter(slug=to_slug).exists()

                while existing:
                    to_slug = slugify(f'{to_slug} {get_random_code()}')
                    existing = Profile.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)


class Relationship(models.Model):
    SEND = 'send'
    ACCEPTED = 'accepted'

    STATUS_CHOICES = (
        (SEND, 'Send'),
        (ACCEPTED, 'Accepted'),
    )

    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self):
        return f'{self.sender}-{self.receiver}-{self.status}'
