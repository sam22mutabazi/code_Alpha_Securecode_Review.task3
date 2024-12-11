# Create your models here.
from django.contrib.auth.models import User  # Importing the built-in User model
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)  # Character field for the title
    content = models.TextField()  # Text field for the content
    published_date = models.DateTimeField(auto_now_add=True)  # DateTime field for publishing date
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to the built-in User model

    def __str__(self):
        return self.title  # This method returns the title when the object is printed
