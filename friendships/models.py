from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Friendship(models.Model):
    from_user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='following_friendship_set')
    to_user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='follower_friendship_set')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (('from_user','created_at'), ('to_user','created_at'))
        unique_together = (('from_user','to_user'),)
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.from_user_id} follow {self.to_user_id}'



