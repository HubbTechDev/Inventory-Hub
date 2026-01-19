# Inventory-Hub

A comprehensive inventory management platform with web scraping capabilities and a complete REST API backend. Extract inventory data from merchant app listings (Mercari, Depop, and more) and manage your inventory through a powerful Flask API.

## Features

### Web Scraping
- 🔍 **Flexible Web Scraping**: Scrape inventory data from various merchant platforms
- 🛍️ **Specialized Scrapers**: Built-in support for **Mercari** and **Depop** marketplaces
- 🎯 **Customizable Selectors**: Configure CSS selectors for different website structures
- 🚀 **JavaScript Support**: Use Selenium for dynamic, JavaScript-rendered content
- 📊 **Multiple Output Formats**: Export data as JSON or CSV
- 🔄 **Multi-page Scraping**: Automatically scrape multiple pages of listings
- 🛡️ **Robust Error Handling**: Built-in retry logic and error recovery
- 📝 **Structured Data Models**: Clean, structured inventory item data

### Backend API
- 🔐 **JWT Authentication**: Secure user authentication and authorization
- 📦 **Inventory Management**: Complete CRUD operations for inventory items
- 🕷️ **Scraping Jobs**: Automated scraping with job tracking and status
- 📊 **Dashboard Statistics**: Comprehensive analytics and insights
- 🔍 **Advanced Search**: Full-text search, filtering, and pagination
- 🌐 **CORS Enabled**: Ready for mobile and web app integration
- 💾 **SQLite/PostgreSQL**: Flexible database support

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
├── backend/                    # Flask REST API
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
├── models.py                  # Scraper data models
├── scraper.py                # Base scraper class
├── mercari_scraper.py        # Mercari scraper
├── depop_scraper.py          # Depop scraper
├── generic_scraper.py        # Generic e-commerce scraper
├── main.py                   # CLI interface
├── config.py                 # Scraper configuration
└── requirements.txt          # Scraper dependencies
```

## Disclaimer

This tool is for educational purposes. Always ensure you have permission to scrape websites and comply with their terms of service and robots.txt files. The developers are not responsible for misuse of this tool.
