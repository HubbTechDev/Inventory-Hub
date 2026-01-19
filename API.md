# API Documentation

REST API documentation for Inventory Hub.

Base URL: `http://localhost:5000/api`

## Authentication

All authenticated endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <your-token>
```

Tokens are obtained through the `/api/auth/login` or `/api/auth/register` endpoints.

---

## Authentication Endpoints

### Register User

Create a new user account.

**Endpoint:** `POST /api/auth/register`

**Request Body:**
```json
{
  "username": "string (3-50 chars, alphanumeric + underscores)",
  "email": "string (valid email format)",
  "password": "string (min 6 chars)"
}
```

**Response:** `201 Created`
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "created_at": "2026-01-19T10:00:00"
  },
  "access_token": "eyJhbGc..."
}
```

**Errors:**
- `400` - Missing required fields or invalid format
- `409` - Username or email already exists

---

### Login

Authenticate a user and get an access token.

**Endpoint:** `POST /api/auth/login`

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:** `200 OK`
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "created_at": "2026-01-19T10:00:00"
  },
  "access_token": "eyJhbGc..."
}
```

**Errors:**
- `400` - Missing username or password
- `401` - Invalid credentials

---

### Get Current User

Get information about the currently authenticated user.

**Endpoint:** `GET /api/auth/me`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "created_at": "2026-01-19T10:00:00"
  }
}
```

---

## Inventory Endpoints

### List Inventory Items

Get a paginated list of inventory items with optional filters.

**Endpoint:** `GET /api/inventory`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `page` (integer, default: 1) - Page number
- `per_page` (integer, default: 20, max: 100) - Items per page
- `merchant` (string) - Filter by merchant name
- `condition` (string) - Filter by condition
- `min_price` (number) - Minimum price filter
- `max_price` (number) - Maximum price filter
- `search` (string) - Search in title/description/brand
- `is_sold` (boolean) - Filter by sold status
- `sort_by` (string) - Sort field (created_at, price, title)
- `sort_order` (string) - Sort order (asc, desc)

**Response:** `200 OK`
```json
{
  "items": [
    {
      "id": 1,
      "title": "Product Name",
      "price": 29.99,
      "currency": "USD",
      "merchant": "Mercari",
      "condition": "new",
      "in_stock": true,
      "is_sold": false,
      "created_at": "2026-01-19T10:00:00",
      ...
    }
  ],
  "total": 100,
  "pages": 5,
  "current_page": 1,
  "per_page": 20,
  "has_next": true,
  "has_prev": false
}
```

---

### Get Single Item

Get details of a specific inventory item.

**Endpoint:** `GET /api/inventory/{id}`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "item": {
    "id": 1,
    "title": "Product Name",
    "price": 29.99,
    "currency": "USD",
    "quantity": null,
    "sku": null,
    "description": "Product description",
    "category": null,
    "brand": null,
    "image_url": "https://example.com/image.jpg",
    "product_url": "https://example.com/product/123",
    "merchant": "Mercari",
    "condition": "new",
    "in_stock": true,
    "scraped_at": "2026-01-19T10:00:00",
    "created_at": "2026-01-19T10:00:00",
    "updated_at": "2026-01-19T10:00:00",
    "tags": [],
    "notes": null,
    "is_sold": false,
    "custom_fields": null
  }
}
```

**Errors:**
- `404` - Item not found

---

### Update Item

Update an inventory item.

**Endpoint:** `PUT /api/inventory/{id}`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "title": "Updated Title",
  "price": 39.99,
  "quantity": 5,
  "description": "Updated description",
  "notes": "Personal notes",
  "tags": "electronics,gadgets",
  "is_sold": true,
  "condition": "used",
  "in_stock": false,
  "category": "Electronics",
  "brand": "BrandName"
}
```

All fields are optional. Only provided fields will be updated.

**Response:** `200 OK`
```json
{
  "message": "Item updated successfully",
  "item": { ... }
}
```

**Errors:**
- `400` - Invalid field values
- `404` - Item not found

---

### Delete Item

Delete an inventory item.

**Endpoint:** `DELETE /api/inventory/{id}`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "message": "Item deleted successfully"
}
```

**Errors:**
- `404` - Item not found

---

### Bulk Delete Items

Delete multiple inventory items at once.

**Endpoint:** `POST /api/inventory/bulk-delete`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "item_ids": [1, 2, 3, 4, 5]
}
```

**Response:** `200 OK`
```json
{
  "message": "Successfully deleted 5 items",
  "deleted": 5
}
```

---

## Scraping Endpoints

### Start Scraping Job

Trigger a new scraping job.

**Endpoint:** `POST /api/scraping/scrape`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "url": "https://www.mercari.com/search/?keyword=shoes",
  "merchant": "mercari",
  "pages": 3
}
```

**Fields:**
- `url` (string, required) - Valid HTTP/HTTPS URL to scrape
- `merchant` (string, default: "Generic") - Merchant platform (mercari, depop, or any custom name)
- `pages` (integer, default: 1, max: 10) - Number of pages to scrape

**Response:** `202 Accepted`
```json
{
  "message": "Scraping job started",
  "job": {
    "id": 1,
    "url": "https://www.mercari.com/search/?keyword=shoes",
    "merchant": "mercari",
    "pages": 3,
    "status": "pending",
    "items_scraped": 0,
    "created_at": "2026-01-19T10:00:00",
    "task_id": "1"
  }
}
```

**Errors:**
- `400` - Missing URL, invalid URL format, or invalid pages value

---

### List Scraping Jobs

Get a list of all scraping jobs for the current user.

**Endpoint:** `GET /api/scraping/jobs`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `page` (integer, default: 1) - Page number
- `per_page` (integer, default: 20, max: 100) - Items per page

**Response:** `200 OK`
```json
{
  "jobs": [
    {
      "id": 1,
      "url": "https://www.mercari.com/search/?keyword=shoes",
      "merchant": "mercari",
      "pages": 3,
      "status": "completed",
      "items_scraped": 45,
      "error_message": null,
      "created_at": "2026-01-19T10:00:00",
      "started_at": "2026-01-19T10:00:01",
      "completed_at": "2026-01-19T10:01:30",
      "task_id": "1"
    }
  ],
  "total": 10,
  "pages": 1,
  "current_page": 1,
  "per_page": 20
}
```

---

### Get Scraping Job

Get details of a specific scraping job.

**Endpoint:** `GET /api/scraping/jobs/{id}`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "job": {
    "id": 1,
    "url": "https://www.mercari.com/search/?keyword=shoes",
    "merchant": "mercari",
    "pages": 3,
    "status": "completed",
    "items_scraped": 45,
    "error_message": null,
    "created_at": "2026-01-19T10:00:00",
    "started_at": "2026-01-19T10:00:01",
    "completed_at": "2026-01-19T10:01:30",
    "task_id": "1"
  }
}
```

**Errors:**
- `404` - Job not found

---

## Statistics Endpoints

### Get Dashboard Statistics

Get comprehensive statistics for the dashboard.

**Endpoint:** `GET /api/stats`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "total_items": 150,
  "total_value": 4567.89,
  "sold_items": 25,
  "unsold_items": 125,
  "total_scraping_jobs": 10,
  "successful_scraping_jobs": 9,
  "items_by_merchant": [
    { "merchant": "Mercari", "count": 100 },
    { "merchant": "Depop", "count": 50 }
  ],
  "items_by_condition": [
    { "condition": "new", "count": 75 },
    { "condition": "used", "count": 75 }
  ],
  "price_distribution": [
    { "range": "0-25", "count": 50 },
    { "range": "25-50", "count": 40 },
    { "range": "50-100", "count": 35 },
    { "range": "100-250", "count": 20 },
    { "range": "250+", "count": 5 }
  ],
  "recent_items": [
    {
      "id": 150,
      "title": "Most Recent Item",
      "price": 29.99,
      ...
    }
  ]
}
```

---

## Error Responses

All endpoints may return these common errors:

### 401 Unauthorized
```json
{
  "msg": "Missing Authorization Header"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

---

## Rate Limiting

Rate limiting is configurable but disabled by default. When enabled:
- Default: 100 requests per minute per IP
- Authentication endpoints: 5 requests per minute
- Exceeding limits returns `429 Too Many Requests`

---

## Data Models

### InventoryItem
```
id: integer
user_id: integer
title: string(500)
price: float
currency: string(10)
quantity: integer
sku: string(100)
description: text
category: string(100)
brand: string(100)
image_url: string(1000)
product_url: string(1000)
merchant: string(100)
condition: string(50)
in_stock: boolean
scraped_at: datetime
created_at: datetime
updated_at: datetime
tags: string(500)
notes: text
is_sold: boolean
custom_fields: json
```

### ScrapingJob
```
id: integer
user_id: integer
url: string(1000)
merchant: string(100)
pages: integer
status: string(50) - pending, running, completed, failed
items_scraped: integer
error_message: text
created_at: datetime
started_at: datetime
completed_at: datetime
task_id: string(255)
```

### User
```
id: integer
username: string(80)
email: string(120)
password_hash: string(255)
created_at: datetime
updated_at: datetime
```

---

For more information, see the [README.md](README.md) or [QUICKSTART.md](QUICKSTART.md).
