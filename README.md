# E-Commerce API

A RESTful API built with **Django REST Framework** for managing products, shopping carts, checkout, and order history. The API includes JWT authentication, product search, price filtering, ordering, pagination, role-based permissions, image uploads, throttling, and interactive API documentation with Swagger.

## Features

### Authentication

* User registration through Djoser.
* JWT authentication for protected API endpoints.
* Access token generation.
* Refresh token support.
* Authenticated users can manage their shopping cart.
* Authenticated users can checkout their cart and view their order history.
* Product creation, updating, and deletion are restricted to admin users.

### Product Management

* List available products.
* Retrieve a specific product.
* Admin users can create products.
* Admin users can update and delete products.

* Products with zero stock are excluded from public product listings.
* Search products by name.
* Filter , Order products by price.
* Pagination is applied to product listings.

### Shopping Cart

* Each user has a personal shopping cart.
* Authenticated users can add products to their cart.
* Adding an existing product increases its quantity by 1.
* Users can decrease the quantity of a cart item.
* The cart response includes the total cost of all cart items.
* Users can only access their own cart.

### Checkout

* Authenticated users can checkout their cart.
* Checkout creates a new order.
* Cart items are converted into order items.
* The product price is stored in the order item as a price snapshot.
* Cart items are deleted after a successful checkout.
* Empty carts cannot be checked out.

### Order History

* Authenticated users can retrieve their order history.
* Users can only retrieve orders belonging to their account.
* Orders store their creation date.
* Each order can contain multiple order items.

### Pagination

Product listings use Django REST Framework's `PageNumberPagination`.

The current page size is:

```text
2 products per page
```

Example:

```text
/products/?page=2
```



## API Endpoints

### Authentication

| **Method** | **Endpoint**         | **Description**                      | **Permission** |
| ---------- | -------------------- | ------------------------------------ | -------------- |
| POST       | `/auth/users/`       | Register a new user                  | Public         |
| POST       | `/auth/jwt/create/`  | Obtain JWT access and refresh tokens | Public         |
| POST       | `/auth/jwt/refresh/` | Refresh an access token              | Public         |

### Products

| **Method** | **Endpoint**      | **Description**            | **Permission** |
| ---------- | ----------------- | -------------------------- | -------------- |
| GET        | `/products/`      | List available products    | Public         |
| POST       | `/products/`      | Create a product           | Admin          |
| GET        | `/products/{id}/` | Retrieve a product         | Public         |
| PUT        | `/products/{id}/` | Update a product           | Admin          |
| PATCH      | `/products/{id}/` | Partially update a product | Admin          |
| DELETE     | `/products/{id}/` | Delete a product           | Admin          |

### Cart

| **Method** | **Endpoint**                  | **Description**                         | **Permission** |
| ---------- | ----------------------------- | --------------------------------------- | -------------- |
| GET        | `/cart/products/`             | Retrieve the user's cart                | Authenticated  |
| POST       | `/cart/products/{id}/`        | Add a product or increase its quantity  | Authenticated  |
| POST       | `/cart/products/{id}/remove/` | Decrease quantity or remove the product | Authenticated  |

### Checkout

| **Method** | **Endpoint** | **Description**           | **Permission** |
| ---------- | ------------ | ------------------------- | -------------- |
| POST       | `/checkout/` | Checkout the current cart | Authenticated  |

### Orders

| **Method** | **Endpoint** | **Description**                   | **Permission** |
| ---------- | ------------ | --------------------------------- | -------------- |
| GET        | `/orders/`   | Retrieve the user's order history | Authenticated  |

## Authentication

This project uses **JWT (JSON Web Token)** authentication.

### Register

Users can register through the Djoser endpoint:

```text
/auth/users/
```

The registration endpoint requires the user's registration information and password confirmation.

### Obtain Tokens

Send a `POST` request to:

```text
/auth/jwt/create/
```

with:

```json
{
    "username": "your_username",
    "password": "your_password"
}
```

The response contains an access token and a refresh token.

Use the access token when accessing protected endpoints:

```text
Authorization: Bearer <access_token>
```

### Refresh Token

Send a `POST` request to:

```text
/auth/jwt/refresh/
```

with:

```json
{
    "refresh": "<refresh_token>"
}
```

The response contains a new access token.

## Cart Workflow

The cart follows this workflow:

```text
Add Product
     ↓
Check User's Cart
     ↓
Product already exists?
     ├── Yes → Increase quantity
     │
     └── No → Create CartItem
```

Removing a product follows:

```text
Remove Product
     ↓
Product exists in cart?
     ├── No → Return 404
     │
     └── Yes
          ↓
     Quantity > 1?
       ├── Yes → Decrease quantity by 1
       │
       └── No → Delete CartItem
```

## Checkout Workflow

The checkout process converts cart items into order items:

```text
POST /checkout/
       ↓
Retrieve user's cart items
       ↓
Check if cart is empty
       ↓
Create Order
       ↓
Create OrderItems
       ↓
Store current product prices
       ↓
Delete CartItems
       ↓
Checkout completed
```

The product price is copied into `OrderItem.price` during checkout so the order retains the purchase price.

## Technologies Used

* Python
* Django
* Django REST Framework
* Djoser
* Simple JWT
* Django Filter
* drf-spectacular
* SQLite

## Performance

The project uses several Django and DRF features to improve API performance:

* `select_related()` is used when retrieving cart items and their related products.
* `prefetch_related()` is used when retrieving products and their many-to-many categories.
* Product prices are indexed using `db_index=True`.
* Product lists are paginated.
* Cart total cost is calculated using Django database aggregation.
* Separate querysets are used to restrict users to their own cart and orders.

## Throttling

The API uses Django REST Framework throttling.

Anonymous users are limited to:

```text
5 requests per minute
```

Authenticated users are limited to:

```text
1000 requests per day
```

These limits are configured using DRF's:

* `AnonRateThrottle`
* `UserRateThrottle`

## Installation

### Prerequisites

* Python 3.12+
* Git
* Virtual environment (recommended)

### 1. Clone the repository

```text
git clone <repository-url>
cd <project-directory>
```

### 2. Create a virtual environment

```text
python -m venv venv
```

Activate it on Windows:

```text
venv\Scripts\activate
```

### 3. Install dependencies

If `requirements.txt` is available:

```text
pip install -r requirements.txt
```

Otherwise, install the required packages:

```text
pip install django djangorestframework djoser djangorestframework-simplejwt django-filter drf-spectacular pillow
```

### 4. Apply migrations

```text
python manage.py migrate
```

### 5. Create a superuser

```text
python manage.py createsuperuser
```

A superuser is required to access Django Admin and the admin-only product management endpoints.

### 6. Run the development server

```text
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

Swagger documentation:

```text
http://127.0.0.1:8000/api/docs/
```

ReDoc:

```text
http://127.0.0.1:8000/api/redoc/
```

OpenAPI schema:

```text
http://127.0.0.1:8000/api/schema/
```

## Project Structure

```text
ECommerce/
│
├── manage.py
├── db.sqlite3
│
├── ECommerce/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── Shop/
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── filters.py
    ├── admin.py
    └── ...
```

### Main Components

* `models.py` — Database models and relationships.
* `serializers.py` — Converts model instances to and from API representations.
* `views.py` — API views and business logic.
* `urls.py` — API endpoint routing.
* `filters.py` — Product price filtering configuration.
* `settings.py` — Django, DRF, JWT, throttling, media, and API documentation configuration.

## API Documentation

Interactive API documentation is available through Swagger UI using **drf-spectacular**.

After starting the development server, visit:

```text
http://127.0.0.1:8000/api/docs/
```

The documentation provides an interactive overview of the available endpoints, request parameters, authentication requirements, and API schemas.

ReDoc is also available at:

```text
http://127.0.0.1:8000/api/redoc/
```

The raw OpenAPI schema is available at:

```text
http://127.0.0.1:8000/api/schema/
```

## Admin Access

Django Admin can be used to manage the application's data.

After creating a superuser:

```text
python manage.py createsuperuser
```

Access Django Admin at:

```text
http://127.0.0.1:8000/admin/
```

Admin users are also required for product creation, updating, and deletion through the API.
