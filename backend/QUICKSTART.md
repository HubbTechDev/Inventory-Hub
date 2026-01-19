# Inventory Hub Backend - Quick Start Guide

## 🚀 Quick Start (5 minutes)

### 1. Setup Backend API

```bash
# Navigate to backend directory
cd backend

# Run automated setup
./setup.sh

# Start the server
./start_server.sh
```

Server will be running at `http://localhost:5000`

### 2. Test the API

**Option A: Run Interactive Demo**
```bash
cd backend
source venv/bin/activate
python api_demo.py
```

**Option B: Use cURL**
```bash
# Health check
curl http://localhost:5000/health

# Register a user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"test123456"}'

# Login and get token
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"test123456"}'
```

**Option C: Import Postman Collection**
1. Open Postman
2. Import `backend/Inventory_Hub_API.postman_collection.json`
3. Start testing!

## 📚 What You Get

### REST API Endpoints

**Authentication**
- ✅ User registration with JWT tokens
- ✅ Login/logout functionality  
- ✅ Token refresh mechanism
- ✅ Password hashing with Werkzeug

**Inventory Management**
- ✅ Create, read, update, delete items
- ✅ Full-text search across title, description, SKU
- ✅ Filter by merchant, category, condition, stock status
- ✅ Pagination support (configurable page size)
- ✅ Sorting by any field (asc/desc)

**Scraping Jobs**
- ✅ Start scraping jobs for Mercari, Depop, or custom sites
- ✅ Track job status (pending, running, completed, failed)
- ✅ View scraped items per job
- ✅ Automatic integration with existing scrapers
- ✅ Error handling and retry logic

**Dashboard Statistics**
- ✅ Total inventory count and value
- ✅ Items by merchant breakdown
- ✅ Items by condition breakdown
- ✅ Top categories
- ✅ Scraping job success rates
- ✅ Recent activity tracking

### Database Models

**Users**
- Secure password storage
- Email and username uniqueness
- Timestamps for audit trail

**Inventory Items**
- Complete product information
- Custom fields support (JSON)
- Relationship to scraping jobs
- User ownership

**Scraping Jobs**
- Job status tracking
- Performance metrics (duration, items count)
- Error logging
- User association

## 🛠️ Development

### Running Tests

```bash
cd backend
source venv/bin/activate
python test_setup.py
```

### Database Management

```bash
# Access the database
cd backend
source venv/bin/activate
python

>>> from app import create_app
>>> from models import db, User, InventoryItem
>>> app = create_app()
>>> with app.app_context():
...     users = User.query.all()
...     print(f"Total users: {len(users)}")
```

### API Testing Workflow

1. **Register** a new user → Get access token
2. **Create** inventory items manually or via scraping
3. **List** items with filters and search
4. **Update** items as needed
5. **View** dashboard statistics
6. **Start** scraping jobs to import new items
7. **Track** job progress and results

## 🔒 Security Features

- ✅ JWT-based authentication
- ✅ Password hashing with bcrypt
- ✅ CORS configuration for cross-origin requests
- ✅ Input validation on all endpoints
- ✅ SQL injection protection via SQLAlchemy
- ✅ User isolation (users only see their own data)

## 📱 Mobile App Integration

The API is ready for mobile app development:

```javascript
// Example: React Native / Expo
const API_URL = 'http://localhost:5000/api';

// Register user
const register = async (username, email, password) => {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, email, password })
  });
  const data = await response.json();
  return data.access_token;
};

// Get inventory
const getInventory = async (token, page = 1) => {
  const response = await fetch(`${API_URL}/inventory?page=${page}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return response.json();
};

// Start scraping
const startScraping = async (token, url, merchant) => {
  const response = await fetch(`${API_URL}/scraping/scrape`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ url, merchant, max_pages: 1 })
  });
  return response.json();
};
```

## 🚀 Production Deployment

### 1. Database

Switch to PostgreSQL for production:

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb inventory_hub

# Update .env
DATABASE_URL=postgresql://username:password@localhost/inventory_hub
```

### 2. Environment Variables

```bash
# Generate strong secrets
export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
export JWT_SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')

# Set production mode
export FLASK_ENV=production
export FLASK_DEBUG=False

# Configure CORS
export CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

### 3. WSGI Server

Use Gunicorn for production:

```bash
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 "backend.app:create_app('production')"
```

### 4. Reverse Proxy (Nginx)

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 5. SSL/HTTPS

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d api.yourdomain.com
```

## 📊 Performance Tips

1. **Database Indexing**: Already configured on key fields (user_id, merchant, category, etc.)
2. **Pagination**: Use page size limits to prevent large queries
3. **Caching**: Consider Redis for frequently accessed data
4. **Connection Pooling**: SQLAlchemy handles this automatically
5. **Background Jobs**: Use Celery for long-running scraping tasks

## 🐛 Troubleshooting

**Server won't start:**
```bash
# Check port availability
lsof -i :5000

# Kill existing process if needed
kill -9 $(lsof -t -i:5000)
```

**Database errors:**
```bash
# Reset database
cd backend
rm inventory_hub.db
python -c "from app import create_app; from models import db; app = create_app(); app.app_context().push(); db.create_all()"
```

**Import errors:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

## 📖 Additional Resources

- [Full API Documentation](README.md)
- [Postman Collection](Inventory_Hub_API.postman_collection.json)
- [Interactive Demo](api_demo.py)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

## 🎯 Next Steps

1. ✅ Setup completed - Server running
2. 📱 Build mobile app using the API
3. 🎨 Create frontend dashboard
4. 🔧 Customize scrapers for additional merchants
5. 📊 Add analytics and reporting features
6. 🚀 Deploy to production

---

**Ready to build something amazing! 🚀**
