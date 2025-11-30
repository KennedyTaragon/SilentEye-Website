from django.contrib import admin
from ..models.team import TeamMember # Adjusted import for standard structure


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'order', 'is_active']
    
    # --- RECOMMENDED ADDITION ---
    # Allows the admin to change 'order' and 'is_active' directly 
    # from the team list view without opening each member's form.
    list_editable = ['order', 'is_active'] 
    
    list_filter = ['is_active']
    search_fields = ['name', 'position', 'bio', 'email'] # Added search fields for usability
    
    fieldsets = (
        (None, {'fields': ('name', 'position', 'bio', 'photo')}),
        ('Contact & Display', {'fields': ('email', 'linkedin_url', 'order', 'is_active')}),
    )