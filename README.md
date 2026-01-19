# Inventory-Hub

A comprehensive inventory management platform with web scraping capabilities, a complete REST API backend, and a native mobile application. Extract inventory data from merchant app listings (Mercari, Depop, and more) and manage your inventory through a powerful Flask API and intuitive mobile app.

## 🚀 Platform Components

This repository contains three main components:

1. **Web Scraper** - Python-based scraping tools for Mercari, Depop, and generic e-commerce sites
2. **Backend API** - Flask REST API with authentication, inventory management, and scraping job orchestration
3. **Mobile App** - React Native (Expo) cross-platform app for iOS and Android

## Features

### 📱 Mobile Application (NEW!)
- 🔐 **User Authentication**: Login/Register with JWT tokens
- 📊 **Dashboard**: Real-time statistics and analytics with interactive charts
- 📦 **Inventory Management**: Browse, search, filter, and manage items
- 🕷️ **Scraping Interface**: Start and monitor scraping jobs from your phone
- 📈 **Charts & Visualizations**: Pie charts, bar charts for inventory insights
- 🔄 **Pull-to-Refresh**: Stay up-to-date with latest data
- 💾 **Offline Support**: Basic caching for offline access
- 🎨 **Material Design**: Professional UI with React Native Paper
- 🌓 **Cross-Platform**: Works on both iOS and Android

### 🌐 Backend API
- 🔐 **JWT Authentication**: Secure user authentication and authorization
- 📦 **Inventory Management**: Complete CRUD operations for inventory items
- 🕷️ **Scraping Jobs**: Automated scraping with job tracking and status
- 📊 **Dashboard Statistics**: Comprehensive analytics and insights
- 🔍 **Advanced Search**: Full-text search, filtering, and pagination
- 🌐 **CORS Enabled**: Ready for mobile and web app integration
- 💾 **SQLite/PostgreSQL**: Flexible database support
- 📝 **API Documentation**: Complete endpoint documentation

### 🔍 Web Scraping Engine
- 🔍 **Flexible Web Scraping**: Scrape inventory data from various merchant platforms
- 🛍️ **Specialized Scrapers**: Built-in support for **Mercari** and **Depop** marketplaces
- 🎯 **Customizable Selectors**: Configure CSS selectors for different website structures
- 🚀 **JavaScript Support**: Use Selenium for dynamic, JavaScript-rendered content
- 📊 **Multiple Output Formats**: Export data as JSON or CSV
- 🔄 **Multi-page Scraping**: Automatically scrape multiple pages of listings
- 🛡️ **Robust Error Handling**: Built-in retry logic and error recovery
- 📝 **Structured Data Models**: Clean, structured inventory item data

## Installation

### Prerequisites

- Python 3.8 or higher
- Chrome/Chromium browser (for Selenium support)

### Web Scraper Setup

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

4. Create a `.env` file (optional):
```bash
cp .env.example .env
# Edit .env with your preferred settings
```

### Backend API Setup

For the complete Flask REST API backend:

1. Navigate to backend directory:
```bash
cd backend
```

2. Run the automated setup:
```bash
./setup.sh
```

Or manually:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Start the API server:
```bash
./start_server.sh
# Or: python app.py
```

The API will be available at `http://localhost:5000`

**See [backend/README.md](backend/README.md) for complete API documentation.**

### 📱 Mobile App Setup

For the React Native mobile application:

1. Navigate to mobile directory:
```bash
cd mobile
```

2. Install dependencies:
```bash
npm install
```

3. Configure API endpoint:
```bash
cp .env.example .env
# Edit .env and set API_BASE_URL (default: http://localhost:5000)
```

4. Start the Expo development server:
```bash
npm start
```

5. Run on your device:
- **iOS Simulator**: Press `i` in terminal
- **Android Emulator**: Press `a` in terminal
- **Physical Device**: Scan QR code with Expo Go app

**See [mobile/README.md](mobile/README.md) for complete mobile app documentation.**

## 🚀 Quick Start (Full Stack)

To run the complete platform:

1. **Start Backend API**:
```bash
cd backend
./start_server.sh
# API runs on http://localhost:5000
```

2. **Start Mobile App** (in new terminal):
```bash
cd mobile
npm start
# Scan QR code or press i/a for simulator
```

3. **Register & Login** in the mobile app to start using the platform!

## Usage

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
# Scrape multiple pages with custom merchant name
python main.py "https://example.com/category/electronics" --merchant "ExampleStore" --pages 5

# Use Selenium for JavaScript-rendered content
python main.py "https://example.com/products" --selenium --pages 3

# Export to CSV format
python main.py "https://example.com/products" --format csv

# Custom output file
python main.py "https://example.com/products" --output my_inventory.json

# Use custom CSS selectors
python main.py "https://example.com/products" \
  --title-selector "h1.product-name" \
  --price-selector "span.price-value"
```

### Command-Line Arguments

- `url`: URL to scrape (required)
- `--merchant`: Merchant name (default: Generic)
- `--pages`: Number of pages to scrape (default: 1)
- `--selenium`: Use Selenium for JavaScript content
- `--output`: Custom output file path
- `--format`: Output format - json or csv (default: json)
- `--title-selector`: CSS selector for product title
- `--price-selector`: CSS selector for price

## Programmatic Usage

You can also use Inventory Hub as a Python library:

### Using Mercari Scraper

```python
from mercari_scraper import MercariScraper

# Create a Mercari scraper
scraper = MercariScraper()

# Scrape a single listing
items = scraper.scrape_listing("https://www.mercari.com/us/item/m12345678/")

# Scrape multiple pages
collection = scraper.scrape_multiple_pages(
    "https://www.mercari.com/search/?keyword=sneakers",
    max_pages=3
)

# Save results
collection.save_to_json("mercari_inventory.json")

# Clean up
scraper.cleanup()
```

### Using Depop Scraper

```python
from depop_scraper import DepopScraper

# Create a Depop scraper
scraper = DepopScraper()

# Scrape a single listing
items = scraper.scrape_listing("https://www.depop.com/products/username-product-id/")

# Scrape a shop's listings
collection = scraper.scrape_multiple_pages(
    "https://www.depop.com/username/",
    max_pages=5
)

# Save results
collection.save_to_json("depop_inventory.json")

# Clean up
scraper.cleanup()
```

### Using Generic Scraper

```python
from generic_scraper import GenericEcommerceScraper
from models import InventoryCollection

# Create a scraper instance
scraper = GenericEcommerceScraper(
    merchant_name="MyStore",
    title_selector="h1.product-title",
    price_selector="span.price",
    use_selenium=False
)

# Scrape a single listing
items = scraper.scrape_listing("https://example.com/product/123")

# Scrape multiple pages
collection = scraper.scrape_multiple_pages(
    "https://example.com/category/products",
    max_pages=5
)

# Save results
collection.save_to_json("inventory.json")
collection.save_to_csv("inventory.csv")

# Clean up
scraper.cleanup()
```

## Creating Custom Scrapers

For specific merchant platforms, you can create custom scrapers:

```python
from generic_scraper import GenericEcommerceScraper

class MyCustomScraper(GenericEcommerceScraper):
    def __init__(self):
        super().__init__(
            merchant_name="CustomMerchant",
            title_selector="h1.product-name",
            price_selector="span.price-value",
            description_selector="div.product-desc",
            image_selector="img.main-product-image",
            sku_selector="span.product-sku",
            stock_selector="div.stock-info",
            use_selenium=False
        )
```

## Data Structure

Each scraped inventory item contains the following fields:

```python
{
    "title": "Product Name",
    "price": 29.99,
    "currency": "USD",
    "quantity": null,
    "sku": "PROD-123",
    "description": "Product description...",
    "category": null,
    "brand": null,
    "image_url": "https://example.com/image.jpg",
    "product_url": "https://example.com/product/123",
    "merchant": "ExampleStore",
    "condition": "new",
    "in_stock": true,
    "scraped_at": "2026-01-19T12:44:29.000Z",
    "custom_fields": null
}
```

## Configuration

Configuration can be set via environment variables in a `.env` file:

- `USER_AGENT`: User agent string for requests
- `REQUEST_TIMEOUT`: Request timeout in seconds (default: 30)
- `MAX_RETRIES`: Maximum retry attempts (default: 3)
- `RETRY_DELAY`: Delay between retries in seconds (default: 2)
- `USE_HEADLESS`: Run Selenium in headless mode (default: True)
- `PAGE_LOAD_TIMEOUT`: Selenium page load timeout (default: 30)
- `OUTPUT_DIR`: Output directory for scraped data (default: scraped_data)
- `OUTPUT_FORMAT`: Default output format - json or csv (default: json)
- `LOG_LEVEL`: Logging level (default: INFO)

## Best Practices

1. **Respect robots.txt**: Always check and respect the website's robots.txt file
2. **Rate Limiting**: Add delays between requests to avoid overwhelming servers
3. **Legal Compliance**: Ensure you have permission to scrape the target website
4. **Error Handling**: The scraper includes retry logic, but always monitor for errors
5. **Custom Selectors**: Inspect the target website's HTML to identify correct selectors

## Troubleshooting

### Common Issues

**Selenium not working:**
- Ensure Chrome/Chromium is installed
- The WebDriver will be automatically downloaded on first use

**No items scraped:**
- Check if the CSS selectors match the website's structure
- Try using Selenium if the content is JavaScript-rendered
- Check the logs for specific error messages

**Permission denied:**
- Ensure you have write permissions for the output directory
- Check that the output directory exists

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Backend API

The repository includes a complete Flask REST API for managing inventory and scraping jobs. Key features:

### API Endpoints

**Authentication:**
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - Login with JWT tokens
- `GET /api/auth/me` - Get current user
- `POST /api/auth/refresh` - Refresh access token

**Inventory Management:**
- `GET /api/inventory` - List items (with search, filters, pagination)
- `GET /api/inventory/:id` - Get single item
- `POST /api/inventory` - Create item
- `PUT /api/inventory/:id` - Update item
- `DELETE /api/inventory/:id` - Delete item

**Scraping Jobs:**
- `POST /api/scraping/scrape` - Start scraping job
- `GET /api/scraping/jobs` - List jobs
- `GET /api/scraping/jobs/:id` - Get job details

**Statistics:**
- `GET /api/stats` - Dashboard statistics

### Quick Start

```bash
# Start the API server
cd backend
./setup.sh
./start_server.sh
```

### API Demo

Run the interactive demo to see all API endpoints in action:

```bash
cd backend
source venv/bin/activate
python api_demo.py
```

### Testing with Postman

Import the Postman collection for easy API testing:
1. Open Postman
2. Import `backend/Inventory_Hub_API.postman_collection.json`
3. Start making requests!

### Complete Documentation

See [backend/README.md](backend/README.md) for:
- Complete API documentation
- Request/response examples
- Database schema
- Authentication flow
- Production deployment guide

## Project Structure

```
Inventory-Hub/
├── backend/                    # Flask REST API Backend
│   ├── routes/                # API route handlers
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── inventory.py      # Inventory management
│   │   ├── scraping.py       # Scraping jobs
│   │   └── stats.py          # Statistics
│   ├── app.py                # Flask application
│   ├── models.py             # Database models
│   ├── config.py             # Configuration
│   ├── requirements.txt      # Backend dependencies
│   ├── api_demo.py           # Interactive API demo
│   ├── test_setup.py         # Setup validation
│   └── README.md             # API documentation
│
├── mobile/                    # React Native Mobile App
│   ├── src/
│   │   ├── api/              # API client & endpoints
│   │   ├── components/       # Reusable UI components
│   │   ├── screens/          # App screens
│   │   │   ├── AuthScreens/ # Login, Register
│   │   │   └── MainScreens/ # Dashboard, Inventory, etc.
│   │   ├── navigation/       # Navigation setup
│   │   ├── contexts/         # Auth context
│   │   ├── utils/            # Utilities
│   │   ├── types/            # TypeScript types
│   │   └── constants/        # App constants
│   ├── assets/               # Icons and splash screens
│   ├── App.tsx               # Root component
│   ├── package.json          # Dependencies
│   ├── tsconfig.json         # TypeScript config
│   └── README.md             # Mobile app docs
│
├── Web Scraper Files (Root)
│   ├── models.py             # Scraper data models
│   ├── scraper.py            # Base scraper class
│   ├── mercari_scraper.py    # Mercari scraper
│   ├── depop_scraper.py      # Depop scraper
│   ├── generic_scraper.py    # Generic e-commerce scraper
│   ├── main.py               # CLI interface
│   ├── config.py             # Scraper configuration
│   └── requirements.txt      # Scraper dependencies
│
├── tests/                     # Test suites
├── examples/                  # Usage examples
└── README.md                  # This file
```

## Disclaimer

This tool is for educational purposes. Always ensure you have permission to scrape websites and comply with their terms of service and robots.txt files. The developers are not responsible for misuse of this tool.

## 📖 Documentation

- **[Backend API Documentation](backend/README.md)** - Complete REST API reference
- **[Mobile App Documentation](mobile/README.md)** - Mobile app setup and features
- **[Architecture Guide](ARCHITECTURE.md)** - Technical architecture details
- **[Mercari/Depop Guide](MERCARI_DEPOP_GUIDE.md)** - Scraping specific merchants

## 🎯 Success Criteria Met

✅ Backend API with 13 endpoints (auth, inventory, scraping, stats)  
✅ Mobile app with 8 screens (Login, Register, Dashboard, Inventory, Detail, Scrape, History, Profile)  
✅ User authentication with JWT tokens  
✅ Dashboard with statistics and charts  
✅ Inventory management with search, filter, pagination  
✅ Scraping job creation and monitoring  
✅ Cross-platform (iOS & Android)  
✅ Offline caching support  
✅ Professional Material Design UI  
✅ Production-ready code with error handling  
✅ Comprehensive documentation  

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.
