from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import CustomUser
from api.models import Organisation, Role, Member
import time

@receiver(post_save, sender=CustomUser)
def create_organisation_and_member(sender, instance, created, **kwargs):
    if created:
        # Create a new Organisation
        org = Organisation.objects.create(
            name=instance.email.split('@')[0],  # or another way to set the name
            status=0,
            personal=False,
            settings={},
            created_at=int(time.time()),  # example timestamp
            updated_at=int(time.time())
        )
        
        # Create roles
        owner_role = Role.objects.create(
            name='Owner',
            description='Owner role',
            org_id=org
        )
        member_role = Role.objects.create(
            name='Member',
            description='Member role',
            org_id=org
        )
        
        # Assign the new user as the owner of the organisation
        Member.objects.create(
            org_id=org,
            user_id=instance,
            role_id=owner_role,
            status=0,
            settings={},
            created_at=int(time.time()),
            updated_at=int(time.time())
        )
