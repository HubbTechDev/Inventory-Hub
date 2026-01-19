# Inventory Hub - Architecture Overview

## Project Structure

```
Inventory-Hub/
├── README.md                          # Main documentation
├── MERCARI_DEPOP_GUIDE.md            # Mercari & Depop specific guide
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment configuration template
├── .gitignore                         # Git ignore rules
│
├── Core Modules
│   ├── models.py                      # Data models (InventoryItem, InventoryCollection)
│   ├── config.py                      # Configuration management
│   ├── scraper.py                     # BaseScraper abstract class
│   ├── generic_scraper.py             # GenericEcommerceScraper implementation
│   ├── mercari_scraper.py             # MercariScraper implementation
│   ├── depop_scraper.py               # DepopScraper implementation
│   └── main.py                        # CLI entry point
│
├── examples/
│   ├── custom_scrapers.py             # Example custom scraper implementations
│   ├── usage_examples.py              # General usage examples
│   └── mercari_depop_examples.py      # Mercari & Depop specific examples
│
└── tests/
    ├── test_models.py                 # Tests for data models
    └── test_mercari_depop.py          # Tests for Mercari & Depop scrapers
```

## Component Hierarchy

```
┌─────────────────────────────────────────────────┐
│              BaseScraper (Abstract)             │
│  - HTML fetching (requests + Selenium)          │
│  - Retry logic & error handling                 │
│  - Resource cleanup                             │
└────────────┬────────────────────────────────────┘
             │
             ├─────────────────────────────────────┐
             │                                     │
┌────────────▼──────────────┐      ┌──────────────▼─────────────┐
│  GenericEcommerceScraper  │      │  Platform-Specific         │
│  - Customizable selectors │      │  Scrapers                  │
│  - Works with most sites  │      │                            │
└───────────────────────────┘      ├────────────────────────────┤
                                   │  MercariScraper            │
                                   │  - Mercari-specific logic  │
                                   │  - USD pricing             │
                                   │  - Condition normalization │
                                   ├────────────────────────────┤
                                   │  DepopScraper              │
                                   │  - Depop-specific logic    │
                                   │  - Multi-currency support  │
                                   │  - Size extraction         │
                                   └────────────────────────────┘
```

## Data Flow

```
1. User Input
   └─> URL + Configuration

2. Scraper Selection
   ├─> MercariScraper (if --merchant mercari)
   ├─> DepopScraper (if --merchant depop)
   └─> GenericEcommerceScraper (otherwise)

3. Data Fetching
   ├─> HTTP Request (requests library)
   └─> JavaScript Rendering (Selenium WebDriver)

4. HTML Parsing
   └─> BeautifulSoup + CSS Selectors

5. Data Extraction
   ├─> Title, Price, Description
   ├─> SKU, Brand, Category
   ├─> Images, Condition
   └─> Custom Fields (e.g., size for Depop)

6. Data Modeling
   └─> InventoryItem objects

7. Collection
   └─> InventoryCollection

8. Export
   ├─> JSON file
   └─> CSV file
```

## Key Features by Scraper

### BaseScraper (Abstract)
- ✅ HTTP requests with retry logic
- ✅ Selenium integration for JS-rendered content
- ✅ Resource management (context manager support)
- ✅ Error handling and logging

### GenericEcommerceScraper
- ✅ Customizable CSS selectors
- ✅ Works with most e-commerce platforms
- ✅ Single and multi-page scraping
- ✅ Price extraction from various formats

### MercariScraper
- ✅ Mercari-specific selectors
- ✅ SKU extraction from URL
- ✅ Condition normalization (new, like new, good, fair, poor, used)
- ✅ Sold item detection
- ✅ USD currency
- ✅ Brand and category extraction

### DepopScraper
- ✅ Depop-specific selectors
- ✅ Multi-currency support (USD, GBP, EUR)
- ✅ Size information extraction
- ✅ SKU extraction from URL
- ✅ Condition normalization
- ✅ Sold item detection
- ✅ Custom fields for additional data

## Usage Patterns

### Command Line Interface
```bash
# Generic scraper
python main.py "https://example.com/product" --pages 5

# Mercari scraper
python main.py "https://www.mercari.com/..." --merchant mercari

# Depop scraper
python main.py "https://www.depop.com/..." --merchant depop
```

### Programmatic Usage
```python
# Import specific scraper
from mercari_scraper import MercariScraper

# Use context manager for automatic cleanup
with MercariScraper() as scraper:
    collection = scraper.scrape_multiple_pages(url, max_pages=5)
    collection.save_to_json("output.json")
```

## Dependencies

### Core Libraries
- **beautifulsoup4** - HTML parsing
- **lxml** - Fast XML/HTML parser
- **requests** - HTTP library
- **selenium** - Browser automation
- **webdriver-manager** - Automatic WebDriver management
- **python-dotenv** - Environment variable management

### Optional Libraries
- **pandas** - Advanced data manipulation (for CSV export)

## Configuration

Environment variables (via `.env` file):
- `USER_AGENT` - HTTP user agent string
- `REQUEST_TIMEOUT` - Request timeout in seconds
- `MAX_RETRIES` - Maximum retry attempts
- `USE_HEADLESS` - Run browser in headless mode
- `OUTPUT_DIR` - Output directory path
- `OUTPUT_FORMAT` - Default output format (json/csv)
- `LOG_LEVEL` - Logging verbosity

## Testing

### Test Coverage
- ✅ Data model tests (InventoryItem, InventoryCollection)
- ✅ Scraper initialization tests
- ✅ Price extraction tests
- ✅ Condition normalization tests
- ✅ Currency detection tests (Depop)
- ✅ Size extraction tests (Depop)
- ✅ Context manager tests

### Running Tests
```bash
# All tests
python -m unittest discover tests -v

# Specific test file
python -m unittest tests.test_models -v
python -m unittest tests.test_mercari_depop -v
```

## Future Enhancements

Potential additions:
- [ ] Additional marketplace scrapers (Poshmark, eBay, etc.)
- [ ] Database storage support (SQLite, PostgreSQL)
- [ ] Rate limiting configuration
- [ ] Proxy support
- [ ] Image downloading
- [ ] Product comparison features
- [ ] Price tracking over time
- [ ] Web interface/dashboard
- [ ] API endpoints

## Legal & Ethical Considerations

⚠️ **Important**: This tool is for educational purposes. Users must:
- Respect robots.txt files
- Follow platform terms of service
- Avoid overloading servers
- Only scrape publicly available data
- Consider API alternatives when available
- Comply with data protection laws
