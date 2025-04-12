from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
# imports for user registration page 
from django.db import models
from django.contrib.auth.models import User


User = get_user_model()

class Collection(models.Model):
    """
    Collection model to group machinery
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Machinery(models.Model):
    """
    Machinery model to store machinery information.
    """
    STATUS_CHOICES = (
        ('OK', 'OK'),
        ('WARNING', 'Warning'),
        ('FAULT', 'Fault'),
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OK')
    importance = models.IntegerField(default=0, help_text="Higher value means more important")
    collections = models.ManyToManyField(Collection, related_name='machinery', blank=True)
    assigned_technicians = models.ManyToManyField(
        User,
        related_name='assigned_machinery_tech',
        blank=True,
        limit_choices_to={'groups__name': 'Technicians'}
    )
    assigned_repair = models.ManyToManyField(
        User,
        related_name='assigned_machinery_repair',
        blank=True,
        limit_choices_to={'groups__name': 'Repair'}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_status(self):
        """Update the status based on warnings and faults"""
        if self.faults.filter(resolved=False).exists():
            self.status = 'FAULT'
        elif self.warnings.exists():
            self.status = 'WARNING'
        else:
            self.status = 'OK'
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-importance', 'name']
        verbose_name_plural = "Machinery"


class MachineryWarning(models.Model):
    """
    Warning model to store machinery warnings.
    """
    machinery = models.ForeignKey(Machinery, on_delete=models.CASCADE, related_name='warnings')
    text = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_warnings')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.machinery.update_status()

    def delete(self, *args, **kwargs):
        machinery = self.machinery
        super().delete(*args, **kwargs)
        machinery.update_status()

    def __str__(self):
        return f"{self.machinery.name}: {self.text}"

    class Meta:
        unique_together = ('machinery', 'text')


class MachineryFault(models.Model):
    """
    MachineryFault model to store machinery fault cases.
    """
    machinery = models.ForeignKey(Machinery, on_delete=models.CASCADE, related_name='faults')
    title = models.CharField(max_length=100)
    details = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_faults')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='resolved_faults',
                                    blank=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new or self._state.adding is False:
            self.machinery.update_status()

    def __str__(self):
        return f"Case #{self.pk}: {self.title}"

    class Meta:
        ordering = ['-created_at']


class FaultImage(models.Model):
    """
    Images related to fault cases.
    """
    fault = models.ForeignKey(MachineryFault, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='fault_images/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.fault}"


class FaultComment(models.Model):
    """
    Comments on fault cases.
    """
    fault = models.ForeignKey(MachineryFault, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.fault}"

    class Meta:
        ordering = ['created_at']

# userregistration class 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - {self.role}"



