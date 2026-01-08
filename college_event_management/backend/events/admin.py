from django.contrib import admin

from .models import Category, Event, EventCoordinator, EventResource, Venue


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('venue_name', 'location', 'capacity', 'availability_status')
    list_filter = ('availability_status', 'has_projector', 'has_sound_system')
    search_fields = ('venue_name', 'location')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Venue Information', {
            'fields': ('venue_name', 'location', 'capacity', 'facilities')
        }),
        ('Amenities', {
            'fields': ('has_projector', 'has_sound_system')
        }),
        ('Status', {
            'fields': ('availability_status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'icon')
    search_fields = ('category_name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'venue', 'department', 'status', 'current_registrations', 'max_capacity')
    list_filter = ('status', 'event_type', 'event_date', 'department', 'category')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at', 'current_registrations')
    
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'description', 'poster_image', 'event_type', 'category')
        }),
        ('Scheduling', {
            'fields': ('event_date', 'start_time', 'end_time', 'registration_deadline')
        }),
        ('Location & Capacity', {
            'fields': ('venue', 'max_capacity', 'current_registrations')
        }),
        ('Organization', {
            'fields': ('department', 'created_by')
        }),
        ('Fees & Status', {
            'fields': ('registration_fee', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class EventResourceInline(admin.TabularInline):
    model = EventResource
    extra = 1


class EventCoordinatorInline(admin.TabularInline):
    model = EventCoordinator
    extra = 1


@admin.register(EventCoordinator)
class EventCoordinatorAdmin(admin.ModelAdmin):
    list_display = ('event', 'faculty', 'role', 'assigned_date')
    list_filter = ('assigned_date', 'role')
    search_fields = ('event__title', 'faculty__email')


@admin.register(EventResource)
class EventResourceAdmin(admin.ModelAdmin):
    list_display = ('event', 'resource_name', 'resource_type', 'quantity', 'status', 'cost')
    list_filter = ('resource_type', 'status', 'event')
    search_fields = ('resource_name', 'event__title')
