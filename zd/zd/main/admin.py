from django.contrib import admin
from .models import CustomUser, Application, Project, ProjectRequirement, ProjectInvitation, ProjectParticipant, ProjectFile, ProjectComment

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'middle_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization_name', 'contact_first_name', 'contact_last_name', 'contact_email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('organization_name', 'contact_email', 'contact_first_name', 'contact_last_name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Organization Info', {
            'fields': ('organization_name', 'organization_inn', 'organization_website', 'user')
        }),
        ('Solution Info', {
            'fields': ('solution_name', 'solution_description', 'solution_experience')
        }),
        ('Contact Info', {
            'fields': ('contact_first_name', 'contact_last_name', 'contact_middle_name', 
                      'contact_phone', 'contact_email')
        }),
        ('Skills & Requirements', {
            'fields': ('skill_list', 'requirement_name', 'requirement_price')
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'creator', 'status', 'budget', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'description', 'creator__email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'creator', 'status')
        }),
        ('Детали проекта', {
            'fields': ('team_activities', 'work_conditions')
        }),
        ('Сроки и бюджет', {
            'fields': ('start_date', 'end_date', 'budget')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    inlines = []  # Добавим инлайны позже

class ProjectRequirementInline(admin.TabularInline):
    model = ProjectRequirement
    extra = 1
    fields = ('skill_name', 'level_requirement', 'people_count', 'is_mandatory', 'price', 'work_condition')

@admin.register(ProjectRequirement)
class ProjectRequirementAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'skill_name', 'level_requirement', 'people_count', 'is_mandatory', 'price')
    list_filter = ('level_requirement', 'is_mandatory', 'project')
    search_fields = ('skill_name', 'project__name')
    raw_id_fields = ('project',)

class ProjectParticipantInline(admin.TabularInline):
    model = ProjectParticipant
    extra = 0
    fields = ('full_name', 'email', 'role', 'status')
    readonly_fields = ('joined_at',)

@admin.register(ProjectParticipant)
class ProjectParticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'project', 'role', 'status', 'joined_at')
    list_filter = ('status', 'role', 'project')
    search_fields = ('full_name', 'email', 'project__name')
    raw_id_fields = ('project', 'application', 'user')
    readonly_fields = ('joined_at', 'left_at')

@admin.register(ProjectInvitation)
class ProjectInvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'application', 'invited_by', 'status', 'invited_at')
    list_filter = ('status', 'invited_at')
    search_fields = ('project__name', 'application__contact_email')
    raw_id_fields = ('project', 'application', 'invited_by')
    readonly_fields = ('invited_at', 'responded_at')
    actions = ['accept_invitations', 'decline_invitations']

    def accept_invitations(self, request, queryset):
        for invitation in queryset:
            invitation.accept()
        self.message_user(request, f"{queryset.count()} приглашений принято")
    accept_invitations.short_description = "Принять выбранные приглашения"

    def decline_invitations(self, request, queryset):
        for invitation in queryset:
            invitation.decline()
        self.message_user(request, f"{queryset.count()} приглашений отклонено")
    decline_invitations.short_description = "Отклонить выбранные приглашения"

@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'filename', 'project', 'uploaded_by', 'file_size', 'uploaded_at')
    list_filter = ('uploaded_at', 'project')
    search_fields = ('filename', 'description')
    raw_id_fields = ('project', 'uploaded_by')
    readonly_fields = ('file_size', 'uploaded_at')

@admin.register(ProjectComment)
class ProjectCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'project', 'short_text', 'created_at')
    list_filter = ('created_at', 'project')
    search_fields = ('text', 'author__email')
    raw_id_fields = ('project', 'author', 'parent')
    readonly_fields = ('created_at', 'updated_at')

    def short_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    short_text.short_description = 'Текст комментария'

# Обновляем ProjectAdmin с инлайнами
ProjectAdmin.inlines = [ProjectRequirementInline, ProjectParticipantInline]