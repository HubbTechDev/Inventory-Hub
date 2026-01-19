# Quick Start Guide

Get started with Inventory Hub in just a few minutes!

## Prerequisites

- Python 3.8 or higher
- Chrome/Chromium browser (for web scraping)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/HubbTechDev/Inventory-Hub.git
   cd Inventory-Hub
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database:**
   ```bash
   python init_db.py
   ```

5. **Start the application:**
   ```bash
   python run.py
   ```

6. **Open your browser:**
   - Navigate to `http://localhost:5000`
   - The frontend will be served automatically

## First Steps

### 1. Create an Account

1. Click "Register" on the homepage
2. Enter your username, email, and password
3. Click "Register" - you'll be logged in automatically

### 2. Scrape Your First Inventory

1. Click "Scraping" in the navigation menu
2. Enter a URL (try: `https://www.mercari.com/search/?keyword=shoes`)
3. Select merchant platform (Mercari, Depop, or Generic)
4. Choose number of pages to scrape (1-10)
5. Click "Start Scraping"
6. Wait for the job to complete

### 3. View Your Inventory

1. Click "Inventory" in the navigation menu
2. See all scraped items in the table
3. Use filters to search by merchant, condition, or keyword
4. Click "Delete" to remove items

### 4. Check Your Dashboard

1. Click "Dashboard" to see:
   - Total items and value
   - Items by merchant
   - Items by condition
   - Recently added items

## Using the Command Line

You can also use the CLI for quick scraping:

```bash
# Scrape a Mercari listing
python main.py "https://www.mercari.com/us/item/m12345678/" --merchant mercari

# Scrape multiple pages
python main.py "https://www.mercari.com/search/?keyword=shoes" --merchant mercari --pages 3

# Export to CSV
python main.py "https://example.com/products" --format csv
```

## Docker Quick Start

If you prefer Docker:

```bash
# Start all services
docker-compose up -d

# Initialize database (first time only)
docker-compose exec web python init_db.py

# Access the application
# Open http://localhost:5000 in your browser

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## API Quick Start

You can also interact with the API directly:

### Register a User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'
```

### Start Scraping (with token from login)
```bash
curl -X POST http://localhost:5000/api/scraping/scrape \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.mercari.com/search/?keyword=test","merchant":"mercari","pages":1}'
```

### Get Inventory
```bash
curl -X GET http://localhost:5000/api/inventory \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Troubleshooting

### Port 5000 already in use
```bash
# Change the port in .env file
PORT=5001

# Or run with custom port
FLASK_APP=backend.app:app flask run --port 5001
```

### Database errors
```bash
# Re-initialize the database
rm -f instance/inventory_hub.db
python init_db.py
```

### Selenium/Chrome errors
- Make sure Chrome/Chromium is installed
- The WebDriver will be automatically downloaded on first use
- Try running without `--selenium` flag first

## Next Steps

- Read the [README.md](README.md) for detailed documentation
- Check [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Explore the API endpoints
- Customize scrapers for other platforms

## Need Help?

- Open an issue on GitHub
- Check existing issues and discussions
- Read the full documentation in README.md

Happy scraping! 🎉
