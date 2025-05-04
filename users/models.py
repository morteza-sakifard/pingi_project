from django.db import models

class User(models.Model):
    mobile = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    now_request_count = models.IntegerField(default=0)

    def __str__(self):
        return self.mobile