from django.db import models
from django.contrib.auth.models import Permission
# Create your models here.
class User(models.Model):
    """
    User model to store user information.
    """
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    AccessGroup = models.ForeignKey('Group', on_delete=models.CASCADE)
    def __str__(self):
        return self.username

class Group(models.Model):
    """
    Group model to store user group information.
    """
    name = models.CharField(max_length=150, unique=True)
    # permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name

class Machinery(models.Model):
    """
    Machinery model to store machinery information.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    warnings = models.CharField(blank=True, max_length=100)
    MachineryFault = models.ForeignKey('MachineryFault', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

class MachineryFault(models.Model):
    """
    MachineryFault model to store machinery fault information.
    """
    FaultID = models.AutoField(primary_key=True)
    Details = models.TextField()
    FaultTime = models.DateTimeField(auto_now_add=True)
    Image = models.ImageField(upload_to='media/', blank=True, null=True)

    def __str__(self):
        return self.name

