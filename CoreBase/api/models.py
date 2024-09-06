import uuid 
from django.db import models
from users.models import CustomUser  
from django.conf import settings

class Organisation(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    status = models.IntegerField(default=0, null=False)
    personal = models.BooleanField(default=False, null=True)
    settings = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.BigIntegerField(null=True, blank=True)
    updated_at = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    org_id = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name

class Member(models.Model):
    org_id = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=False)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE, null=False)
    status = models.IntegerField(default=0, null=False)
    settings = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.BigIntegerField(null=True, blank=True)
    updated_at = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Member {self.user_id} in {self.org_id}"



class Invitation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('expired', 'Expired'),
    ]
    
    org_id = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='invitations')
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)   

    def __str__(self):
        return f"Invitation for {self.user_id} to {self.org_id}"