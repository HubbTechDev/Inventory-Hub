# Mercari and Depop Scraper Quick Reference

## Overview

This document provides a quick reference for using the Mercari and Depop scrapers included in the Inventory Hub application.

## Mercari Scraper

### Features
- Scrapes product listings from Mercari marketplace
- Extracts: title, price, SKU, description, condition, brand, category, images
- Supports multi-page scraping
- Uses Selenium for JavaScript-rendered content
- Auto-detects sold items

### Command Line Usage

```bash
# Single product
python main.py "https://www.mercari.com/us/item/m12345678/" --merchant mercari

# Search results (multiple pages)
python main.py "https://www.mercari.com/search/?keyword=vintage+shoes" \
  --merchant mercari --pages 5 --format json

# Export to CSV
python main.py "https://www.mercari.com/search/?keyword=sneakers" \
  --merchant mercari --pages 3 --format csv --output mercari_sneakers.csv
```

### Programmatic Usage

```python
from mercari_scraper import MercariScraper

scraper = MercariScraper()

# Single item
items = scraper.scrape_listing("https://www.mercari.com/us/item/m12345678/")
print(f"Product: {items[0].title} - ${items[0].price}")

# Multiple pages
collection = scraper.scrape_multiple_pages(
    "https://www.mercari.com/search/?keyword=vintage+shirt",
    max_pages=3
)
collection.save_to_json("mercari_shirts.json")

scraper.cleanup()
```

### Extracted Data Fields

| Field | Description | Example |
|-------|-------------|---------|
| title | Product title | "Vintage Nike Sneakers" |
| price | Price in USD | 45.00 |
| sku | Mercari item ID | "MERC-12345678" |
| description | Product description | "Gently used, great condition" |
| condition | Normalized condition | "good", "like new", "new", etc. |
| brand | Product brand | "Nike" |
| category | Product category | "Shoes > Sneakers" |
| image_url | Main product image | URL string |
| in_stock | Availability status | true/false (false if sold) |

## Depop Scraper

### Features
- Scrapes product listings from Depop marketplace
- Extracts: title, price, SKU, description, condition, brand, category, size, images
- Multi-currency support (USD, GBP, EUR)
- Supports multi-page scraping
- Uses Selenium for JavaScript-rendered content
- Auto-detects sold items
- Stores size in custom_fields

### Command Line Usage

```bash
# Single product
python main.py "https://www.depop.com/products/username-product-id/" --merchant depop

# Shop listings (multiple pages)
python main.py "https://www.depop.com/username/" \
  --merchant depop --pages 10 --format json

# Search results
python main.py "https://www.depop.com/search/?q=vintage+jacket" \
  --merchant depop --pages 5 --format csv
```

### Programmatic Usage

```python
from depop_scraper import DepopScraper

scraper = DepopScraper()

# Single item
items = scraper.scrape_listing("https://www.depop.com/products/user-item/")
item = items[0]
print(f"Product: {item.title} - {item.currency} {item.price}")
if item.custom_fields and 'size' in item.custom_fields:
    print(f"Size: {item.custom_fields['size']}")

# Shop/category pages
collection = scraper.scrape_multiple_pages(
    "https://www.depop.com/username/",
    max_pages=5
)
collection.save_to_json("depop_shop.json")

scraper.cleanup()
```

### Extracted Data Fields

| Field | Description | Example |
|-------|-------------|---------|
| title | Product title | "Vintage Band T-Shirt" |
| price | Price (numeric) | 25.00 |
| currency | Currency code | "USD", "GBP", "EUR" |
| sku | Depop product ID | "DEPOP-username-product-id" |
| description | Product description | "Vintage 90s band tee" |
| condition | Normalized condition | "used", "like new", "new" |
| brand | Product brand | "Vintage" |
| category | Product category | "Tops > T-Shirts" |
| image_url | Main product image | URL string |
| in_stock | Availability status | true/false (false if sold) |
| custom_fields.size | Clothing size | "M", "L", "10", etc. |

## Multi-Merchant Scraping

You can scrape from both platforms and combine the results:

```python
from mercari_scraper import MercariScraper
from depop_scraper import DepopScraper
from models import InventoryCollection

# Combined collection
combined = InventoryCollection()

# Scrape Mercari
with MercariScraper() as mercari:
    mercari_items = mercari.scrape_multiple_pages(
        "https://www.mercari.com/search/?keyword=sneakers",
        max_pages=3
    )
    combined.add_items(mercari_items.items)

# Scrape Depop
with DepopScraper() as depop:
    depop_items = depop.scrape_multiple_pages(
        "https://www.depop.com/search/?q=sneakers",
        max_pages=3
    )
    combined.add_items(depop_items.items)

# Save combined results
combined.save_to_json("all_sneakers.json")
print(f"Total items: {len(combined)}")
```

## Best Practices

### Rate Limiting
- Add delays between requests (built-in 2-second delay in multi-page scraping)
- Avoid scraping too many pages at once
- Be respectful of server resources

### Error Handling
- Scrapers include retry logic for failed requests
- Failed items are logged but don't stop the scraping process
- Always use context managers or call `cleanup()` to free resources

### Legal Compliance
- Check and respect robots.txt
- Review platform terms of service
- Only scrape publicly available data
- Consider API alternatives if they become available

## Troubleshooting

### Common Issues

**Selenium WebDriver errors:**
- Ensure Chrome/Chromium is installed
- WebDriver is auto-downloaded on first use
- Check `USE_HEADLESS` setting in .env

**Empty results:**
- Selectors may need updating if site changes
- Enable logging to see detailed error messages
- Try using `--selenium` flag for dynamic content

**Slow performance:**
- Selenium is slower than regular requests
- Reduce `max_pages` parameter
- Scraping is sequential to avoid rate limiting

## Configuration

Create a `.env` file for custom settings:

```bash
# Selenium settings
USE_HEADLESS=True
PAGE_LOAD_TIMEOUT=30

# Output settings
OUTPUT_DIR=scraped_data
OUTPUT_FORMAT=json

# Request settings
REQUEST_TIMEOUT=30
MAX_RETRIES=3
RETRY_DELAY=2

# Logging
LOG_LEVEL=INFO
```

## Support

For issues, questions, or contributions, please visit the GitHub repository.
