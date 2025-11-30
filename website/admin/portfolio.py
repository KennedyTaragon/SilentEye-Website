from django.contrib import admin
from ..models import Client, Testimonial


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo']
    search_fields = ['name']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'company']
    search_fields = ['name', 'company', 'quote']