from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-property/', views.add_property, name='add_property'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('my-properties/', views.my_properties, name='my_properties'),
    path('edit-property/<int:pk>/', views.edit_property, name='edit_property'),
    path('delete-property/<int:pk>/', views.delete_property, name='delete_property'),
    path('favorite/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),
    path('my-favorites/', views.my_favorites, name='my_favorites'),
    path('my-inquiries/', views.my_inquiries, name='my_inquiries'),

    
    # DRF API ROUTES
    
    path('api/properties/', views.api_property_list, name='api-property-list'),
    path('api/properties/<int:pk>/', views.api_property_detail, name='api-property-detail'),
    path('api/properties/create/', views.api_property_create, name='api-property-create'),
    path('api/properties/update/<int:pk>/', views.api_property_update, name='api-property-update'),
    path('api/properties/delete/<int:pk>/', views.api_property_delete, name='api-property-delete'),
    path('api/reviews/', views.api_reviews, name='api-reviews'),
    path('api/inquiries/', views.api_inquiries, name='api-inquiries'),
    path('api/favorites/', views.api_favorites, name='api-favorites'),
    path('api/profiles/', views.api_profiles, name='api-profiles'),
]