from django.contrib import admin
from .models import Organisation, Role, Member, Invitation

@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'status', 'personal', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('status', 'personal')
    ordering = ('-created_at',)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'description', 'org_id')
    search_fields = ('name', 'description')
    list_filter = ('org_id',)
    ordering = ('name',)

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('id','user_id', 'org_id', 'role_id', 'status', 'created_at', 'updated_at')
    search_fields = ('user_id__username', 'org_id__name', 'role_id__name')
    list_filter = ('org_id', 'role_id', 'status')
    ordering = ('-created_at',)




@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('org_id', 'user_id', 'token', 'status', 'created_at', 'expires_at')
    search_fields = ('user_id__username', 'org_id__name', 'token')
    list_filter = ('status', 'org_id')
    ordering = ('-created_at',)
