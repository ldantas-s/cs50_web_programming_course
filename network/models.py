import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(
            User, on_delete=models.CASCADE, related_name="post"
    )
    content = models.CharField(max_length=255, default=None)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f"{self.user} to {self.content}"


class Follower(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )

    def __str__(self):
        return f"{self.following} -> {self.follower}"

    class Meta:
        unique_together = (("follower", "following"),)


class Like(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="like_post", default=None
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="like_user", default=None
    )

    def __str__(self):
        return f"{self.post} : {self.user}"

    class Meta:
        unique_together = (("post", "user"),)
