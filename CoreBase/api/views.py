from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Invitation, Organisation, CustomUser, Member, Role 
from .serializers import InvitationSerializer
import time 
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404






class StatOrgMemberView(APIView):
    def get(self, request, *args, **kwargs):
        # Retrieve query parameters from request
        org_id = request.GET.get('org_id')
        role = request.GET.get('role')

        if org_id is not None:
            org_id = int(org_id)
        if org_id is not None and role is not None:
            try:
                count = Role.objects.filter(org_id=org_id, name=role).count() 
                org_id = int(org_id)
                return Response({"number_of_members_in_the_organization": count})
            except ValueError:
                return Response({"error": "Invalid org_id format"}, status=400)
        
        count = Role.objects.count()
        return Response({"number of member in the organisation":count}) 



class SendInvitationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        
        user = request.user
        org_id = request.data.get('org_id')
        try:
            org = Organisation.objects.get(id=org_id)
        except Organisation.DoesNotExist:
            return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)

        if not org.members.filter(user_id=user, role_id__name='Owner').exists():
            return Response({'error': 'Only owners can send invitations'}, status=status.HTTP_403_FORBIDDEN)

        invitation = Invitation.objects.create(
            org_id=org,
            user_id=CustomUser.objects.get(id=request.data.get('user_id')),
            expires_at=timezone.now() + timezone.timedelta(days=1)  
        )

        return Response({'token': str(invitation.token)}, status=status.HTTP_201_CREATED)

class AcceptInvitationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        token = request.data.get('token')
        try:
            invitation = Invitation.objects.get(token=token)
        except Invitation.DoesNotExist:
            return Response({'error': 'Invitation not found'}, status=status.HTTP_404_NOT_FOUND)

        if invitation.status != 'pending':
            return Response({'error': 'Invitation is not valid'}, status=status.HTTP_400_BAD_REQUEST)

        if timezone.now() > invitation.expires_at:
            invitation.status = 'expired'
            invitation.save()
            return Response({'error': 'Invitation has expired'}, status=status.HTTP_400_BAD_REQUEST)

        
        user = request.user
        if user != invitation.user_id:
            return Response({'error': 'User does not match the invitation'}, status=status.HTTP_403_FORBIDDEN)

        invitation.status = 'accepted'
        invitation.save()

        
        org_id = invitation.org_id
        org = Organisation.objects.get(name=org_id)
        if org:
            Member.objects.create(
                org_id=org,
                user_id=user,
                role_id=Role.objects.get(name='Member', org_id=org),
                status=0,
                created_at=int(time.time()),
                updated_at=int(time.time())
            )

        return Response({'message': 'Invitation accepted and user added to the organization'}, status=status.HTTP_200_OK)


class PromoteMemberAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        org_name = request.data.get('org_name')
        member_email = request.data.get('member_email')

        if org_name != user.email.split('@')[0]:
            return Response({'error': 'You are not authorized to assign roles in this organization'}, status=status.HTTP_403_FORBIDDEN)
  
        user_member = get_object_or_404(CustomUser, email=member_email)

        org = get_object_or_404(Organisation, name=org_name)

        try:
            member = Member.objects.get(org_id=org, user_id=user_member)
        except Member.DoesNotExist:
            return Response({'error': 'This user has to join the organization before their role can be updated'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            admin_role = Role.objects.get(org_id=org, name='Admin')
            member.role_id = admin_role
            member.updated_at = int(time.time())  # Set updated_at to current timestamp
            member.save()
        except Role.DoesNotExist:
            return Response({'error': 'Admin role not found in the organization'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'Member has been promoted to admin successfully'}, status=status.HTTP_200_OK)