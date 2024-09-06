from django.urls import path
from .views import SendInvitationAPIView, AcceptInvitationAPIView, PromoteMemberAPIView, StatOrgMemberView

urlpatterns = [
    path('invite/', SendInvitationAPIView.as_view(), name='send_invitation'),
    path('accept_invitation/', AcceptInvitationAPIView.as_view(), name='accept_invitation'),
    path('promote_member/', PromoteMemberAPIView.as_view(), name='promote_member'),
    path('stat_org_member/', StatOrgMemberView.as_view(), name='stat_org_number'), 
]
