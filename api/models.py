from django.db import models
from django.contrib.auth.models import User
class Articles(models.Model):
    header = models.CharField(max_length=50)
    body = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return f"{self.header} - {self.body}, created_at: {self.created_at}, user: {self.user}"