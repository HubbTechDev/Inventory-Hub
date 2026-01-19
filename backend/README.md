# Inventory Hub Backend API

A complete Flask-based REST API for the Inventory Hub scraping application. This backend provides authentication, inventory management, web scraping jobs, and dashboard statistics.

## Features

- 🔐 **JWT Authentication** - Secure user authentication with access and refresh tokens
- 📦 **Inventory Management** - Full CRUD operations for inventory items
- 🕷️ **Web Scraping** - Integrate with existing Mercari, Depop, and generic e-commerce scrapers
- 📊 **Dashboard Statistics** - Comprehensive analytics and insights
- 🔍 **Search & Filters** - Advanced search, filtering, and pagination
- 🌐 **CORS Enabled** - Ready for mobile app integration

## Tech Stack

- **Flask** - Web framework
- **SQLAlchemy** - ORM and database management
- **Flask-JWT-Extended** - JWT authentication
- **Flask-CORS** - Cross-origin resource sharing
- **SQLite** - Database (easily replaceable with PostgreSQL/MySQL)

## Installation

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables (optional):**
   ```bash
   cp ../.env.example .env
   ```
   
   Edit `.env` to configure:
   - `SECRET_KEY` - Flask secret key
   - `JWT_SECRET_KEY` - JWT secret key
   - `DATABASE_URL` - Database connection string
   - `FLASK_ENV` - development/production

4. **Run the server:**
   ```bash
   python app.py
   ```

   The API will be available at `http://localhost:5000`

## API Documentation

### Base URL
```
http://localhost:5000/api
```

### Authentication

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": "2024-01-15T10:30:00"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password"
}
```

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer {access_token}
```

#### Refresh Token
```http
POST /api/auth/refresh
Authorization: Bearer {refresh_token}
```

---

### Inventory Management

#### List Inventory Items
```http
GET /api/inventory?page=1&per_page=20&search=laptop&merchant=Mercari&condition=new&in_stock=true
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `page` (int) - Page number (default: 1)
- `per_page` (int) - Items per page (default: 20, max: 100)
- `search` (string) - Search in title, description, SKU
- `merchant` (string) - Filter by merchant
- `category` (string) - Filter by category
- `condition` (string) - Filter by condition
- `in_stock` (boolean) - Filter by stock status
- `sort_by` (string) - Sort field (default: created_at)
- `sort_order` (string) - asc/desc (default: desc)

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "title": "Vintage Nike Shoes",
      "price": 45.99,
      "currency": "USD",
      "quantity": 1,
      "sku": "MERC-123456",
      "description": "Great condition vintage shoes",
      "category": "Shoes",
      "brand": "Nike",
      "condition": "used",
      "image_url": "https://...",
      "product_url": "https://...",
      "merchant": "Mercari",
      "in_stock": true,
      "custom_fields": {"size": "10"},
      "scraped_at": "2024-01-15T10:00:00",
      "created_at": "2024-01-15T10:05:00",
      "updated_at": "2024-01-15T10:05:00",
      "job_id": 1
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total_items": 150,
    "total_pages": 8,
    "has_next": true,
    "has_prev": false
  }
}
```

#### Get Single Item
```http
GET /api/inventory/{id}
Authorization: Bearer {access_token}
```

#### Create Item
```http
POST /api/inventory
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Custom Product",
  "price": 99.99,
  "currency": "USD",
  "quantity": 5,
  "sku": "CUSTOM-001",
  "description": "Product description",
  "category": "Electronics",
  "brand": "Apple",
  "condition": "new",
  "image_url": "https://...",
  "product_url": "https://...",
  "merchant": "Custom",
  "in_stock": true,
  "custom_fields": {"warranty": "2 years"}
}
```

#### Update Item
```http
PUT /api/inventory/{id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "price": 89.99,
  "quantity": 3,
  "in_stock": true
}
```

#### Delete Item
```http
DELETE /api/inventory/{id}
Authorization: Bearer {access_token}
```

---

### Scraping Jobs

#### Start Scraping Job
```http
POST /api/scraping/scrape
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "url": "https://www.mercari.com/search/?keyword=vintage",
  "merchant": "Mercari",
  "max_pages": 3
}
```

**Parameters:**
- `url` (string, required) - URL to scrape
- `merchant` (string, required) - Merchant name (Mercari, Depop, or custom)
- `max_pages` (int, optional) - Number of pages to scrape (1-10, default: 1)

**Response:**
```json
{
  "message": "Scraping completed successfully. 25 items scraped.",
  "job": {
    "id": 5,
    "user_id": 1,
    "merchant": "Mercari",
    "url": "https://www.mercari.com/search/?keyword=vintage",
    "status": "completed",
    "items_scraped": 25,
    "error_message": null,
    "created_at": "2024-01-15T11:00:00",
    "started_at": "2024-01-15T11:00:05",
    "completed_at": "2024-01-15T11:02:30",
    "duration_seconds": 145.5
  }
}
```

#### List Scraping Jobs
```http
GET /api/scraping/jobs?page=1&per_page=20&status=completed
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `page` (int) - Page number
- `per_page` (int) - Jobs per page
- `status` (string) - Filter by status (pending, running, completed, failed)

#### Get Job Details
```http
GET /api/scraping/jobs/{id}
Authorization: Bearer {access_token}
```

**Response includes all items scraped in the job:**
```json
{
  "job": {
    "id": 5,
    "merchant": "Mercari",
    "url": "https://...",
    "status": "completed",
    "items_scraped": 25,
    "items": [
      {
        "id": 101,
        "title": "Product 1",
        ...
      }
    ]
  }
}
```

---

### Dashboard Statistics

#### Get Statistics
```http
GET /api/stats
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "inventory": {
    "total_items": 250,
    "items_in_stock": 200,
    "items_out_of_stock": 50,
    "total_value": 12500.50,
    "items_last_week": 45,
    "items_last_month": 180
  },
  "merchants": [
    {"merchant": "Mercari", "count": 120},
    {"merchant": "Depop", "count": 80},
    {"merchant": "Generic", "count": 50}
  ],
  "conditions": [
    {"condition": "new", "count": 100},
    {"condition": "used", "count": 120},
    {"condition": "like new", "count": 30}
  ],
  "categories": [
    {"category": "Electronics", "count": 60},
    {"category": "Clothing", "count": 90},
    {"category": "Shoes", "count": 45}
  ],
  "scraping_jobs": {
    "total_jobs": 25,
    "successful_jobs": 22,
    "failed_jobs": 2,
    "pending_jobs": 1,
    "recent_jobs": [...]
  }
}
```

---

## Database Schema

### Users
- `id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `password_hash`
- `created_at`
- `updated_at`

### Inventory Items
- `id` (Primary Key)
- `user_id` (Foreign Key → Users)
- `job_id` (Foreign Key → Scraping Jobs, nullable)
- `title`
- `price`
- `currency`
- `quantity`
- `sku`
- `description`
- `category`
- `brand`
- `condition`
- `image_url`
- `product_url`
- `merchant`
- `in_stock`
- `custom_fields` (JSON)
- `scraped_at`
- `created_at`
- `updated_at`

### Scraping Jobs
- `id` (Primary Key)
- `user_id` (Foreign Key → Users)
- `merchant`
- `url`
- `status` (pending, running, completed, failed)
- `items_scraped`
- `error_message`
- `created_at`
- `started_at`
- `completed_at`

---

## Error Handling

All endpoints return consistent error responses:

```json
{
  "error": "Error message describing what went wrong"
}
```

HTTP Status Codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `409` - Conflict (e.g., duplicate username)
- `500` - Internal Server Error

---

## Authentication Flow

1. **Register** or **Login** to get access and refresh tokens
2. Include access token in `Authorization` header for all protected endpoints:
   ```
   Authorization: Bearer {access_token}
   ```
3. When access token expires, use refresh token to get a new access token
4. Access tokens expire after 24 hours (configurable)
5. Refresh tokens expire after 30 days

---

## Supported Scrapers

The API integrates with existing scrapers:

1. **MercariScraper** - For Mercari marketplace
2. **DepopScraper** - For Depop marketplace  
3. **GenericEcommerceScraper** - For other e-commerce sites

Scrapers automatically:
- Extract product information
- Handle pagination
- Save items to database
- Track scraping job status

---

## Development

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests
pytest
```

### Database Migrations
For production, consider using Flask-Migrate:
```bash
pip install Flask-Migrate
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Production Deployment

1. **Use a production database** (PostgreSQL recommended):
   ```bash
   export DATABASE_URL="postgresql://user:pass@localhost/inventory_hub"
   ```

2. **Set strong secrets**:
   ```bash
   export SECRET_KEY="your-strong-secret-key"
   export JWT_SECRET_KEY="your-jwt-secret-key"
   ```

3. **Use a production WSGI server** (Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 "backend.app:create_app('production')"
   ```

4. **Enable HTTPS** with nginx or another reverse proxy

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment (development/production) | development |
| `SECRET_KEY` | Flask secret key | dev-secret-key-change-in-production |
| `JWT_SECRET_KEY` | JWT secret key | Same as SECRET_KEY |
| `DATABASE_URL` | Database connection string | sqlite:///inventory_hub.db |
| `JWT_EXPIRATION_HOURS` | Access token expiration (hours) | 24 |
| `CORS_ORIGINS` | Allowed CORS origins | * |
| `ITEMS_PER_PAGE` | Default pagination size | 20 |
| `MAX_ITEMS_PER_PAGE` | Maximum pagination size | 100 |
| `MAX_SCRAPING_PAGES` | Maximum pages to scrape | 5 |
| `PORT` | Server port | 5000 |
| `HOST` | Server host | 0.0.0.0 |

---

## License

This project is part of the Inventory Hub application.

## Support

For issues and questions, please refer to the main project repository.
