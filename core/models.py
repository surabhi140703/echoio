from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User =get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg= models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location =models.CharField(max_length=100, blank=True)


    def __str__(self) -> str:
        return self.user.username
    
class Post(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4)
    user= models.CharField(max_length=100)
    post_image= models.ImageField(upload_to='post_images')
    title= models.TextField()
    community= models.TextField()
    caption= models.TextField()
    created_at= models.DateTimeField(default=datetime.now)
    no_of_likes= models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.user
    
class LikePost(models.Model):
    post_id= models.CharField(max_length=500)
    username= models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.username
    
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, to_field='id', related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Subcomment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, to_field='id', related_name='subcomments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)




    

