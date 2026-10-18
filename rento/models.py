from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('owner', 'Property Owner'),
        ('tenant', 'Tenant/User'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='tenant')
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Property(models.Model):
    PROPERTY_TYPES = (
        ('Room', 'Room'),
        ('House', 'House'),
        ('Shop', 'Shop'),
        ('Hostel', 'Hostel'),
        ('Apartment', 'Apartment'),
    )
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('rented', 'Rented'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=200)
    description = models.TextField()
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    price = models.IntegerField()
    bedrooms = models.IntegerField(default=1)
    bathrooms = models.IntegerField(default=1)
    area_sqft = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    image = models.ImageField(upload_to='properties/')
    is_furnished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='extra_images')
    image = models.ImageField(upload_to='property_images/')
    caption = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Image for {self.property.title}"


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.property.title} ({self.rating}★)"

    class Meta:
        unique_together = ('property', 'user')


class Inquiry(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('replied', 'Replied'),
        ('closed', 'Closed'),
    )
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry by {self.user.username} for {self.property.title}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')

    def __str__(self):
        return f"{self.user.username} ♥ {self.property.title}"
