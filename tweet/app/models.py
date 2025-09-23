from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField



class Account(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(max_length=100)
    photo = CloudinaryField('image', blank=True, null=True)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="posts")
    heading = models.CharField(max_length=200)   # <-- নতুন যোগ হলো
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def like_count(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.user.name} - {self.heading[:20]}"


# Like model
class Like(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "post")  # একজন ইউজার একবারই like দিতে পারবে

    def __str__(self):

        return f"{self.user.name} liked {self.post.id}"
