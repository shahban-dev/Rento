from rest_framework import serializers
from .models import Property, Review, Inquiry, Favorite, UserProfile


class PropertySerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()

    class Meta:
        model = Property
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = '__all__'


class InquirySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Inquiry
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'