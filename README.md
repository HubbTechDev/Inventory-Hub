# Inventory-Hub

A full-featured web application for scraping, managing, and analyzing inventory data from merchant platforms like Mercari and Depop. This tool provides a complete user experience with a web interface, RESTful API, and powerful scraping capabilities.

## 🌟 Features

### Web Scraping
- 🔍 **Flexible Web Scraping**: Extract inventory data from various merchant platforms
- 🛍️ **Specialized Scrapers**: Built-in support for **Mercari** and **Depop** marketplaces
- 🎯 **Customizable Selectors**: Configure CSS selectors for different website structures
- 🚀 **JavaScript Support**: Use Selenium for dynamic, JavaScript-rendered content
- 🔄 **Multi-page Scraping**: Automatically scrape multiple pages of listings

### Web Application
- 🖥️ **Modern Web Interface**: Responsive dashboard for managing inventory
- 📊 **Interactive Dashboard**: View statistics, charts, and recent items
- 🔐 **User Authentication**: Secure login and registration with JWT tokens
- 📈 **Analytics**: Track inventory by merchant, condition, and price ranges
- 🔍 **Search & Filter**: Find items quickly with powerful filtering
- 📤 **Export Capabilities**: Export inventory data to CSV or JSON

### API & Backend
- 🔌 **RESTful API**: Complete API for all operations
- 💾 **Database Storage**: SQLite/PostgreSQL for persistent data
- 🔒 **Secure**: Password hashing, JWT authentication, input validation
- 📝 **Job Tracking**: Monitor scraping jobs and their status

## 🏗️ Architecture

Inventory-Hub consists of:
- **Backend API** (`/backend`) - Flask REST API with JWT authentication
- **Web Frontend** (`/frontend`) - Browser-based dashboard
- **Mobile App** (`/mobile`) - React Native iOS/Android app

All frontends connect to the same backend API.

## 📱 Mobile App

A native iOS/Android mobile application built with React Native and Expo. Features include:
- 📲 **Cross-Platform**: Single codebase for iOS and Android
- 🔐 **JWT Authentication**: Secure login with token refresh
- 📊 **Full Feature Parity**: Access all inventory management features on mobile
- 📈 **Charts & Analytics**: Visual insights into your inventory
- 🔄 **Real-time Sync**: Pull-to-refresh for latest data
- 🚀 **Upload on the Go**: Trigger and monitor upload jobs from your phone

See [mobile/README.md](mobile/README.md) for iOS/Android app setup instructions.

## 📋 Table of Contents

- [Architecture](#architecture)
- [Mobile App](#mobile-app)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Web Application Usage](#web-application-usage)
- [API Documentation](#api-documentation)
- [Command-Line Usage](#command-line-usage)
- [Docker Deployment](#docker-deployment)
- [Configuration](#configuration)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## ⚡ Quick Start (Easiest Way)

### One-Command Start:

**macOS/Linux:**
```bash
chmod +x quickstart.sh
./quickstart.sh
```

**Windows:**
```cmd
quickstart.bat
```

**All Platforms (Python):**
```bash
python start.py
```

This will:
- ✅ Set up virtual environment
- ✅ Install all dependencies
- ✅ Create configuration files
- ✅ Initialize database
- ✅ Start the web server
- ✅ Open your browser automatically

**That's it!** Your app will be running at http://localhost:5000

---

## 🚀 Manual Installation

### Prerequisites

- Python 3.8 or higher
- Chrome/Chromium browser (for Selenium support)
- Node.js (optional, for frontend development)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/HubbTechDev/Inventory-Hub.git
cd Inventory-Hub
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp .env.example .env
# Edit .env with your preferred settings
```

5. Initialize the database:
```bash
python -c "from backend.app import app; from backend.models import db; app.app_context().push(); db.create_all()"
```

## 🏃 Running the Application

### Start the Web Application

The easiest way is to use `python run.py`:

```bash
python run.py
```

Alternatively, you can use Flask directly:

```bash
# Set Flask app
export FLASK_APP=backend.app:app  # On Windows: set FLASK_APP=backend.app:app

# Run the Flask server
flask run
```

Then open your browser to `http://localhost:5000`.

### Using Docker

```bash
docker-compose up
```

The application will be available at `http://localhost:5000`.

## 🖥️ Web Application Usage

### 1. Register an Account
- Navigate to the application in your browser
- Click "Register" and create an account
- You'll be automatically logged in

### 2. Dashboard
- View total inventory statistics
- See charts showing items by merchant and condition
- Review recently added items

### 3. Scraping Interface
- Click "Scraping" in the navigation menu
- Enter a URL (e.g., `https://www.mercari.com/search/?keyword=shoes`)
- Select the merchant platform (Mercari, Depop, or Generic)
- Choose the number of pages to scrape
- Click "Start Scraping"

### 4. Inventory Management
- Click "Inventory" to view all scraped items
- Use filters to search by merchant, condition, or price
- Click "Delete" to remove items
- Export data to CSV for external analysis

## 📚 API Documentation

### Authentication Endpoints

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

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password"
}
```

Response includes `access_token` for subsequent requests.

### Inventory Endpoints

#### List Inventory
```http
GET /api/inventory?page=1&per_page=20&merchant=mercari
Authorization: Bearer <token>
```

Query parameters:
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)
- `merchant`: Filter by merchant
- `condition`: Filter by condition
- `min_price`: Minimum price
- `max_price`: Maximum price
- `search`: Search in title/description
- `is_sold`: Filter by sold status

#### Get Single Item
```http
GET /api/inventory/{id}
Authorization: Bearer <token>
```

#### Update Item
```http
PUT /api/inventory/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Updated Title",
  "price": 29.99,
  "is_sold": true
}
```

#### Delete Item
```http
DELETE /api/inventory/{id}
Authorization: Bearer <token>
```

### Scraping Endpoints

#### Start Scraping Job
```http
POST /api/scraping/scrape
Authorization: Bearer <token>
Content-Type: application/json

{
  "url": "https://www.mercari.com/search/?keyword=shoes",
  "merchant": "mercari",
  "pages": 3
}
```

#### List Scraping Jobs
```http
GET /api/scraping/jobs?page=1
Authorization: Bearer <token>
```

### Statistics Endpoints

#### Get Dashboard Statistics
```http
GET /api/stats
Authorization: Bearer <token>
```

Returns:
- Total items and value
- Items by merchant
- Items by condition
- Price distribution
- Recent items
- Scraping job statistics

## 💻 Command-Line Usage

You can still use the original CLI for quick scraping tasks:

### Basic Usage

Scrape a single product page:
```bash
python main.py "https://example.com/product/123"
```

### Scraping Mercari Listings

```bash
# Scrape a single Mercari product
python main.py "https://www.mercari.com/us/item/m12345678/" --merchant mercari

# Scrape multiple pages from Mercari search results
python main.py "https://www.mercari.com/search/?keyword=shoes" --merchant mercari --pages 3
```

### Scraping Depop Listings

```bash
# Scrape a single Depop product
python main.py "https://www.depop.com/products/username-product-id/" --merchant depop

# Scrape multiple pages from a Depop shop
python main.py "https://www.depop.com/username/" --merchant depop --pages 5
```

### Advanced Options

```bash
# Use Selenium for JavaScript-rendered content
python main.py "https://example.com/products" --selenium --pages 3

# Export to CSV format
python main.py "https://example.com/products" --format csv

# Custom output file
python main.py "https://example.com/products" --output my_inventory.json
```

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Using Docker Only

```bash
# Build image
docker build -t inventory-hub .

# Run container
docker run -p 5000:5000 -v $(pwd)/scraped_data:/app/scraped_data inventory-hub
```

## ⚙️ Configuration

Configuration is managed through environment variables in a `.env` file:

### Flask Settings
- `SECRET_KEY`: Flask secret key (change in production!)
- `JWT_SECRET_KEY`: JWT token secret (change in production!)
- `DEBUG`: Enable debug mode (default: False)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 5000)

### Database Settings
- `DATABASE_URL`: Database connection string
  - SQLite: `sqlite:///inventory_hub.db`
  - PostgreSQL: `postgresql://user:password@localhost/inventory_hub`

### Scraper Settings
- `USER_AGENT`: User agent for requests
- `REQUEST_TIMEOUT`: Request timeout in seconds
- `MAX_RETRIES`: Maximum retry attempts
- `USE_HEADLESS`: Run Selenium in headless mode
- `PAGE_LOAD_TIMEOUT`: Selenium page load timeout

See `.env.example` for all available options.

## 🛠️ Development

### Project Structure

```
inventory-hub/
├── backend/                # Flask backend application
│   ├── app.py             # Main Flask app
│   ├── config.py          # Configuration settings
│   ├── models.py          # Database models
│   ├── routes/            # API endpoints
│   │   ├── auth.py        # Authentication routes
│   │   ├── inventory.py   # Inventory routes
│   │   ├── scraping.py    # Scraping routes
│   │   └── stats.py       # Statistics routes
│   └── services/          # Business logic
│       └── scraper_service.py
├── frontend/              # Frontend application
│   └── public/            # Static files
│       ├── index.html     # Main HTML
│       ├── style.css      # Styles
│       └── app.js         # JavaScript application
├── scrapers/              # Web scraping modules
│   ├── scraper.py         # Base scraper
│   ├── mercari_scraper.py
│   ├── depop_scraper.py
│   └── generic_scraper.py
├── tests/                 # Test files
├── migrations/            # Database migrations
├── main.py                # CLI entry point
├── models.py              # Data models
├── config.py              # Scraper configuration
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
└── README.md              # This file
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_models.py

# Run with coverage
python -m pytest --cov=backend tests/
```

### Database Migrations

```bash
# Initialize migrations (first time only)
flask db init

# Create a migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## ⚠️ Disclaimer

This tool is for educational purposes. Always ensure you have permission to scrape websites and comply with their terms of service and robots.txt files. The developers are not responsible for misuse of this tool.

## 🙏 Acknowledgments

- Built with Flask, SQLAlchemy, and BeautifulSoup
- Selenium WebDriver for dynamic content scraping
- Special support for Mercari and Depop marketplaces
