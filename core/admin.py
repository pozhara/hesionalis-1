# Imports
from django.contrib import admin
from .models import Artist, Design, Appointment


# Register Artist model
@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'skills', 'gender')
    search_fields = ('name', 'skills', 'gender')
    list_filter = ('name', 'skills', 'gender')


# Register Design model
@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    list_display = ('category', 'artist')
    search_fields = ('category', 'artist')
    list_filter = ('category', 'artist')


# Register Appointment model
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'tattoo_category', 'artist', 'status')
    list_filter = ('status', 'artist', 'created_on')
    search_fields = ('user', 'artist', 'tattoo_category')
    actions = ['accept_appointment', 'reject_appointment']

    # Accept appointments
    def accept_appointment(self, request, queryset):
        queryset.update(status=1)

    # Reject appointments
    def reject_appointment(self, request, queryset):
        queryset.update(status=2)
