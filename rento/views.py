from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.contrib import messages
from .models import Property, Favorite, Inquiry, Review, UserProfile
from .forms import RegisterForm, PropertyForm, InquiryForm, ReviewForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *


# HOME PAGE
def home(request):
    properties = Property.objects.filter(status='available').order_by('-created_at')

    search = request.GET.get('search', '')
    category = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    if search:
        properties = properties.filter(
            Q(city__icontains=search) | Q(title__icontains=search) | Q(address__icontains=search)
        )
    if category:
        properties = properties.filter(property_type=category)
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)

    total_properties = Property.objects.count()
    total_cities = Property.objects.values('city').distinct().count()

    context = {
        'properties': properties,
        'search': search,
        'category': category,
        'min_price': min_price,
        'max_price': max_price,
        'total_properties': total_properties,
        'total_cities': total_cities,
    }
    return render(request, 'rento/home.html', context)


# REGISTER
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = request.POST.get('role', 'tenant')
            phone = request.POST.get('phone', '')
            UserProfile.objects.create(user=user, role=role, phone=phone)
            login(request, user)
            messages.success(request, f'Welcome to Rento, {user.first_name}! Your account has been created.')
            return redirect('home')

    return render(request, 'registration/register.html', {'form': form})


# LOGIN
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('home')

    return render(request, 'registration/login.html', {'form': form})


# LOGOUT
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


# ADD PROPERTY
@login_required
def add_property(request):
    form = PropertyForm()
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.owner = request.user
            prop.save()
            messages.success(request, 'Property listed successfully!')
            return redirect('my_properties')

    return render(request, 'rento/add_property.html', {'form': form})


# PROPERTY DETAIL
def property_detail(request, pk):
    prop = get_object_or_404(Property, id=pk)
    inquiry_form = InquiryForm()
    review_form = ReviewForm()
    reviews = prop.reviews.all().order_by('-created_at')
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg']
    user_has_reviewed = False

    if request.user.is_authenticated:
        user_has_reviewed = reviews.filter(user=request.user).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        if 'inquiry_submit' in request.POST:
            inquiry_form = InquiryForm(request.POST)
            if inquiry_form.is_valid():
                inquiry = inquiry_form.save(commit=False)
                inquiry.user = request.user
                inquiry.property = prop
                inquiry.save()
                messages.success(request, 'Inquiry sent successfully! The owner will contact you.')
                return redirect('property_detail', pk=pk)

        elif 'review_submit' in request.POST and not user_has_reviewed:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.property = prop
                review.save()
                messages.success(request, 'Review posted!')
                return redirect('property_detail', pk=pk)

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, property=prop).exists()

    context = {
        'property': prop,
        'inquiry_form': inquiry_form,
        'review_form': review_form,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'is_favorite': is_favorite,
        'user_has_reviewed': user_has_reviewed,
    }
    return render(request, 'rento/property_detail.html', context)


# MY PROPERTIES
@login_required
def my_properties(request):
    properties = Property.objects.filter(owner=request.user).order_by('-created_at')
    inquiries = Inquiry.objects.filter(property__owner=request.user).order_by('-created_at')[:5]
    return render(request, 'rento/my_properties.html', {
        'properties': properties,
        'inquiries': inquiries,
    })


# EDIT PROPERTY
@login_required
def edit_property(request, pk):
    prop = get_object_or_404(Property, id=pk, owner=request.user)
    form = PropertyForm(instance=prop)

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=prop)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated successfully!')
            return redirect('my_properties')

    return render(request, 'rento/edit_property.html', {'form': form, 'property': prop})


# DELETE PROPERTY
@login_required
def delete_property(request, pk):
    prop = get_object_or_404(Property, id=pk, owner=request.user)
    prop.delete()
    messages.success(request, 'Property deleted.')
    return redirect('my_properties')


# FAVORITE TOGGLE
@login_required
def toggle_favorite(request, pk):
    prop = get_object_or_404(Property, id=pk)
    fav, created = Favorite.objects.get_or_create(user=request.user, property=prop)
    if not created:
        fav.delete()
        messages.info(request, 'Removed from favorites.')
    else:
        messages.success(request, 'Added to favorites!')
    return redirect('property_detail', pk=pk)


# MY FAVORITES
@login_required
def my_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('property').order_by('-added_at')
    return render(request, 'rento/my_favorites.html', {'favorites': favorites})


# MY INQUIRIES
@login_required
def my_inquiries(request):
    inquiries = Inquiry.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'rento/my_inquiries.html', {'inquiries': inquiries})



# DRF APIs

@api_view(['GET'])
def api_property_list(request):

    properties = Property.objects.all()

    serializer = PropertySerializer(
        properties,
        many=True
    )

    return Response(serializer.data)


@api_view(['GET'])
def api_property_detail(request, pk):

    property_obj = get_object_or_404(
        Property,
        id=pk
    )

    serializer = PropertySerializer(
        property_obj
    )

    return Response(serializer.data)


@api_view(['POST'])
def api_property_create(request):

    serializer = PropertySerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response(serializer.data)

    return Response(serializer.errors)


@api_view(['PUT'])
def api_property_update(request, pk):

    property_obj = get_object_or_404(
        Property,
        id=pk
    )

    serializer = PropertySerializer(
        property_obj,
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response(serializer.data)

    return Response(serializer.errors)


@api_view(['DELETE'])
def api_property_delete(request, pk):

    property_obj = get_object_or_404(
        Property,
        id=pk
    )

    property_obj.delete()

    return Response({
        'message': 'Property deleted successfully'
    })


# REVIEWS

@api_view(['GET'])
def api_reviews(request):

    reviews = Review.objects.all()

    serializer = ReviewSerializer(
        reviews,
        many=True
    )

    return Response(serializer.data)


# INQUIRIES

@api_view(['GET'])
def api_inquiries(request):

    inquiries = Inquiry.objects.all()

    serializer = InquirySerializer(
        inquiries,
        many=True
    )

    return Response(serializer.data)


# FAVORITES

@api_view(['GET'])
def api_favorites(request):

    favorites = Favorite.objects.all()

    serializer = FavoriteSerializer(
        favorites,
        many=True
    )

    return Response(serializer.data)


# USER PROFILES

@api_view(['GET'])
def api_profiles(request):

    profiles = UserProfile.objects.all()

    serializer = UserProfileSerializer(
        profiles,
        many=True
    )

    return Response(serializer.data)