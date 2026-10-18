# Rento - Software Requirements Specification

Rento – Property Rental Platform

Software Requirements Specification (SRS)

Muhammad Shaban

F23BDOCS1M01111

BSCS 6th 1M

2023–2027

Web Engineering (Dr. Waqas Sharif)

# 1. Introduction

Rento is a Django-based web application designed to serve as a comprehensive property rental platform for Pakistan. It connects property owners who want to list their spaces with tenants who are searching for rooms, houses, shops, hostels, and apartments. The platform digitizes the traditionally fragmented and phone-driven process of finding and renting property, bringing it into a single, intuitive online system.

Built using Django (backend framework), Django REST Framework (DRF) for API endpoints, Bootstrap 5 (responsive UI), and SQLite (development database), Rento provides a role-based experience for two primary user types: Property Owners and Tenants. Administrators manage the entire platform through Django’s built-in admin panel.

# 2. Problem Statement

The rental property market in Pakistan, particularly in cities like Bahawalpur, Lahore, and Karachi, relies heavily on informal channels: word of mouth, handwritten notices, and phone-based negotiations. This creates the following inefficiencies:

Tenants cannot search, filter, or compare properties remotely, wasting significant time.

Property owners have no digital showcase and rely on physical visits for every inquiry.

There is no structured inquiry system, making communication between parties untracked and unreliable.

Owners receive no reviews or ratings, making trustworthiness difficult to establish.

No centralized record of listings, inquiries, or favorites exists for either party.

Rento addresses all of the above through a fully digital, role-separated platform that centralizes the entire rental discovery and inquiry process.

# 3. How the System Works

## 3.1  Property Owner Workflow

Owner registers and selects the ‘Property Owner’ role during sign-up.

Logs in and navigates to ‘Add Property’ to fill out title, description, city, address, type, price, bedrooms, bathrooms, area, furnishing status, and uploads a cover image.

Listed property appears on the home page and is visible to all visitors.

Owner views incoming inquiries from tenants on the ‘My Properties’ dashboard.

Owner can edit or delete any listing at any time.

## 3.2  Tenant Workflow

Tenant registers and selects the ‘Tenant’ role during sign-up.

Browses the home page; uses search by keyword, category filter, or price range to find properties.

Clicks a property card to view the full detail page with images, specifications, and reviews.

Sends an inquiry message directly to the owner from the detail page.

Saves interesting properties to ‘My Favorites’ for later comparison.

Leaves a star rating and written review after visiting a property.

Tracks all sent inquiries under ‘My Inquiries’ with status (Pending / Replied / Closed).

## 3.3  REST API Layer (DRF)

Rento exposes a full set of JSON API endpoints built with Django REST Framework, enabling future integration with mobile apps or third-party clients:

# 4. Data Models & Database Design

Rento uses six Django ORM models stored in an SQLite database (easily migrated to PostgreSQL for production):

# 5. Technologies & Tools Used

# 6. Key Features & Benefits

## 6.1  For Tenants

Advanced search & filter: find properties by keyword, city, type, and price range in real time.

Detailed property pages with high-resolution images, full specs, and location address.

Star ratings and reviews from previous tenants build trust before committing.

Favorites list allows saving multiple properties for side-by-side comparison.

Inquiry tracker keeps all communications with owners in one place.

## 6.2  For Property Owners

Create and manage multiple property listings with images and detailed descriptions.

Receive structured, time-stamped inquiries from interested tenants.

Edit or delete listings instantly as availability changes.

Online presence eliminates the need for physical notices or newspaper advertisements.

## 6.3  Technical & Business Benefits

REST API layer allows future mobile app development without rewriting backend logic.

Django admin panel gives administrators full CRUD control over all data.

Role-based registration prevents tenants from accidentally listing properties.

Scalable architecture: SQLite can be swapped for PostgreSQL with a single settings change.

Bootstrap 5 ensures the platform is fully usable on phones, tablets, and desktops.

# 7. Future Enhancements

Payment gateway integration (JazzCash / EasyPaisa) for security deposits.

Google Maps integration to show exact property locations on an interactive map.

Real-time chat between tenants and owners using Django Channels (WebSockets).

Email notification system for inquiry replies and status changes.

Mobile application (React Native or Flutter) consuming the existing DRF API.

AI-powered property recommendation engine based on tenant search history.

Lease agreement generation and digital signing.

| Endpoint | Method | Description |
| --- | --- | --- |
| /api/properties/ | GET | List all properties |
| /api/properties/<id>/ | GET | Single property detail |
| /api/properties/create/ | POST | Create a new property |
| /api/properties/update/<id>/ | PUT | Update a property |
| /api/properties/delete/<id>/ | DELETE | Remove a property |
| /api/reviews/ | GET | All reviews |
| /api/inquiries/ | GET | All inquiries |
| /api/favorites/ | GET | All saved favorites |
| /api/profiles/ | GET | All user profiles |

| Model | Purpose & Key Fields |
| --- | --- |
| UserProfile | Extends Django’s User with role (owner/tenant), phone, bio, and profile picture. |
| Property | Core listing: title, description, city, address, type, price, bedrooms, bathrooms, area_sqft, status (available/rented), image, is_furnished. |
| PropertyImage | Additional images linked to a property with optional captions. |
| Review | Tenant-written star rating (1–5) and comment tied to a specific property. One review per user per property enforced. |
| Inquiry | Message sent by a tenant to a property owner with status tracking (Pending / Replied / Closed). |
| Favorite | Many-to-many shortcut between a user and a property. Prevents duplicate saves via unique_together. |

| Layer | Technology | Role |
| --- | --- | --- |
| Backend | Django 4.x (Python) | MVC framework; handles routing, views, ORM, authentication. |
| REST API | Django REST Framework | Serializers and @api_view decorators expose JSON endpoints. |
| Frontend | Bootstrap 5 + HTML5 | Responsive UI grid, cards, modals, and forms. |
| Styling | Custom CSS | Extended Bootstrap with Rento brand colours and layout tweaks. |
| Database | SQLite | Default Django development DB; migrations manage schema. |
| Auth | Django Auth | Session-based login/logout; password hashing; login_required decorator. |
| Media | Pillow (Python) | Image upload handling for property photos and profile pictures. |
| IDE / Tools | VS Code, Git | Development environment and version control. |
