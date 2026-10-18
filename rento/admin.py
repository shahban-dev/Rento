from django.contrib import admin
from .models import Property, Inquiry, Favorite, Review, UserProfile, PropertyImage

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'city', 'property_type', 'price', 'status', 'created_at']
    list_filter = ['property_type', 'status', 'city']
    search_fields = ['title', 'city', 'address']

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['user', 'property', 'status', 'created_at']
    list_filter = ['status']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'property', 'rating', 'created_at']

admin.site.register(Favorite)
admin.site.register(UserProfile)
admin.site.register(PropertyImage)

admin.site.site_header = "Rento Admin Panel"
admin.site.site_title = "Rento"
admin.site.index_title = "Welcome to Rento Administration"
