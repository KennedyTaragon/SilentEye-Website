from django.contrib import admin
from django.urls import reverse
from django.shortcuts import redirect
from ..models import SiteConfig, ContactMessage


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'email', 'phone']

    fieldsets = (
        ("Company Identity", {
            "fields": ('company_name', 'logo', 'email', 'phone', 'address'),
        }),
        ("Social Media & Mapping", {
            "fields": (('facebook_url', 'twitter_url'), ('linkedin_url', 'instagram_url'), 'map_embed_code'),
            "classes": ('collapse',),
        }),
    )

    def changelist_view(self, request, extra_context=None):
        if SiteConfig.objects.exists():
            config = SiteConfig.objects.first()
            url = reverse('admin:website_siteconfig_change', args=[config.pk])
            return redirect(url)
        return super().changelist_view(request, extra_context)

    def has_add_permission(self, request):
        return not SiteConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read', 'phone']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']

    fieldsets = (
        (None, {'fields': ('is_read', 'created_at')}),
        ("Message Details", {'fields': ('name', 'email', 'phone', 'subject', 'message')}),
    )

    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'created_at']

    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} message(s) successfully marked as read.')

    mark_as_read.short_description = "Mark selected messages as read"

    def has_delete_permission(self, request, obj=None):
        return False