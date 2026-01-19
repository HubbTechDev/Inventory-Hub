# Backend Architecture Notes

## Import Structure

### Current Approach
The backend currently uses `sys.path` manipulation to import scrapers from the parent directory:
- `backend/routes/scraping.py` imports from `mercari_scraper`, `depop_scraper`, `generic_scraper`
- `backend/test_setup.py` imports from parent for testing

**Why this approach:**
- Maintains backwards compatibility with existing scraper code
- No need to duplicate scraper files
- Quick setup for development

### Future Improvements

For production and better maintainability, consider:

**Option 1: Package Structure**
```
inventory-hub/
├── setup.py or pyproject.toml
├── inventory_hub/
│   ├── __init__.py
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── mercari.py
│   │   ├── depop.py
│   │   └── generic.py
│   └── api/
│       ├── __init__.py
│       ├── app.py
│       ├── models.py
│       └── routes/
```

Install with: `pip install -e .`

**Option 2: Move Scrapers to Backend**
```
backend/
├── scrapers/
│   ├── __init__.py
│   ├── mercari_scraper.py
│   ├── depop_scraper.py
│   └── generic_scraper.py
└── routes/
    └── scraping.py  # Import: from backend.scrapers import MercariScraper
```

**Option 3: Separate Packages**
- Create `inventory-scrapers` package
- Create `inventory-api` package
- Install both: `pip install inventory-scrapers inventory-api`

## Dependency Management

### Current Approach
- `requirements.txt` with compatible release specifiers (`~=`)
- Allows patch updates for security fixes
- Maintains API compatibility

### Production Recommendations

**For reproducible builds:**
```bash
# Generate locked requirements
pip freeze > requirements-lock.txt

# Or use pip-tools
pip-compile requirements.in
```

**For Docker:**
```dockerfile
# Use specific Python version
FROM python:3.11-slim

# Install exact versions from lock file
COPY requirements-lock.txt .
RUN pip install --no-cache-dir -r requirements-lock.txt
```

## Database Migrations

### Current Approach
- Simple `db.create_all()` for development
- Direct model changes

### Production Recommendations

**Use Flask-Migrate (Alembic):**
```bash
pip install Flask-Migrate

# Initialize migrations
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

Benefits:
- Version control for database schema
- Safe production updates
- Rollback capability

## Testing Strategy

### Current Coverage
- Setup validation tests (`test_setup.py`)
- Basic model and route tests

### Recommended Additions

**Unit Tests:**
```python
# tests/test_models.py
def test_user_password_hashing():
    user = User(username='test', email='test@example.com')
    user.set_password('password123')
    assert user.check_password('password123')
    assert not user.check_password('wrongpass')
```

**Integration Tests:**
```python
# tests/test_api.py
def test_register_and_login(client):
    # Register
    response = client.post('/api/auth/register', json={...})
    assert response.status_code == 201
    
    # Login
    response = client.post('/api/auth/login', json={...})
    assert response.status_code == 200
    assert 'access_token' in response.json
```

**Use pytest framework:**
```bash
pip install pytest pytest-flask

# Run tests
pytest tests/
```

## Security Enhancements

### Current Implementation
- JWT authentication
- Password hashing
- CORS configuration
- Input validation

### Production Additions

**Rate Limiting:**
```bash
pip install Flask-Limiter

# In app.py
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)

# In routes
@limiter.limit("5 per minute")
def login():
    ...
```

**HTTPS Only:**
```python
# Force HTTPS in production
if not app.debug:
    @app.before_request
    def before_request():
        if not request.is_secure:
            url = request.url.replace('http://', 'https://', 1)
            return redirect(url, code=301)
```

**Environment Variables:**
```bash
# Never commit secrets to git
# Use environment variables or secrets manager
export SECRET_KEY=$(openssl rand -hex 32)
export JWT_SECRET_KEY=$(openssl rand -hex 32)
export DATABASE_URL=postgresql://...
```

## Monitoring & Logging

### Production Recommendations

**Structured Logging:**
```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module
        })
```

**Error Tracking:**
- Use Sentry for error tracking
- Log to external service (CloudWatch, Datadog)
- Set up alerts for critical errors

**Performance Monitoring:**
- Use Flask-APM or similar
- Monitor database query performance
- Track API response times

## Deployment Checklist

- [ ] Package structure finalized
- [ ] Database migrations configured
- [ ] Environment variables secured
- [ ] HTTPS enabled
- [ ] Rate limiting implemented
- [ ] Error tracking configured
- [ ] Logging centralized
- [ ] Database backups configured
- [ ] Health checks implemented
- [ ] Documentation updated
- [ ] Load testing completed

## Contributing

When making changes:
1. Update relevant tests
2. Run test suite: `pytest`
3. Update documentation
4. Follow PEP 8 style guide
5. Add docstrings to new functions
6. Update CHANGELOG if applicable
