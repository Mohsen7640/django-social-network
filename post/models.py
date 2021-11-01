from django.db import models
from django.core.validators import FileExtensionValidator

from account.models import Profile


class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    liked = models.ManyToManyField(Profile, blank=True, related_name='likes')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return str(self.content[:20])

    class Meta:
        ordering = ('-created',)

    def num_likes(self):
        return self.liked.all().count()

    def num_comments(self):
        return self.comments.all().count()

    def get_comments(self):
        return self.comments.all()


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)


class Like(models.Model):
    LIKE = 'Like'
    UNLIKE = 'Unlike'

    VALUE_CHOICES = (
        (LIKE, 'Like'),
        (UNLIKE, 'Unlike'),
    )

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    value = models.CharField(choices=VALUE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"
