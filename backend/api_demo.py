#!/usr/bin/env python3
"""
API Demo - Interactive demonstration of the Inventory Hub API
This script shows how to use all API endpoints programmatically.
"""

import requests
import json
import time
from pprint import pprint

# Configuration
BASE_URL = "http://localhost:5000/api"
DEMO_USER = {
    "username": "api_demo_user",
    "email": "apidemo@example.com",
    "password": "demo123456"
}

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")


def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")


def print_info(text):
    print(f"{Colors.CYAN}ℹ {text}{Colors.ENDC}")


def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")


def print_response(response):
    """Print formatted API response."""
    print(f"{Colors.YELLOW}Status: {response.status_code}{Colors.ENDC}")
    if response.status_code < 400:
        pprint(response.json(), indent=2)
    else:
        print_error(response.text)


class InventoryHubAPIDemo:
    def __init__(self):
        self.base_url = BASE_URL
        self.access_token = None
        self.refresh_token = None
        self.headers = {'Content-Type': 'application/json'}
    
    def update_auth_headers(self):
        """Update headers with access token."""
        if self.access_token:
            self.headers['Authorization'] = f'Bearer {self.access_token}'
    
    def demo_health_check(self):
        """Demo: Health check endpoint."""
        print_header("1. Health Check")
        
        response = requests.get(f"{self.base_url.replace('/api', '')}/health")
        print_response(response)
        
        if response.status_code == 200:
            print_success("API is healthy and running!")
    
    def demo_register(self):
        """Demo: User registration."""
        print_header("2. User Registration")
        
        print_info("Registering new user...")
        response = requests.post(
            f"{self.base_url}/auth/register",
            json=DEMO_USER,
            headers=self.headers
        )
        
        print_response(response)
        
        if response.status_code == 201:
            data = response.json()
            self.access_token = data['access_token']
            self.refresh_token = data['refresh_token']
            self.update_auth_headers()
            print_success(f"User registered successfully! User ID: {data['user']['id']}")
        elif response.status_code == 409:
            print_info("User already exists, will login instead...")
            self.demo_login()
    
    def demo_login(self):
        """Demo: User login."""
        print_header("3. User Login")
        
        print_info("Logging in...")
        response = requests.post(
            f"{self.base_url}/auth/login",
            json={
                "username": DEMO_USER['username'],
                "password": DEMO_USER['password']
            },
            headers=self.headers
        )
        
        print_response(response)
        
        if response.status_code == 200:
            data = response.json()
            self.access_token = data['access_token']
            self.refresh_token = data['refresh_token']
            self.update_auth_headers()
            print_success("Login successful!")
    
    def demo_get_current_user(self):
        """Demo: Get current user info."""
        print_header("4. Get Current User")
        
        print_info("Fetching current user info...")
        response = requests.get(
            f"{self.base_url}/auth/me",
            headers=self.headers
        )
        
        print_response(response)
        
        if response.status_code == 200:
            print_success("Retrieved user information!")
    
    def demo_create_inventory_items(self):
        """Demo: Create multiple inventory items."""
        print_header("5. Create Inventory Items")
        
        items = [
            {
                "title": "Vintage Nike Air Jordans",
                "price": 299.99,
                "currency": "USD",
                "quantity": 1,
                "sku": "DEMO-SHOE-001",
                "description": "Classic Air Jordan 1 in excellent condition",
                "category": "Shoes",
                "brand": "Nike",
                "condition": "used",
                "merchant": "Mercari",
                "in_stock": True
            },
            {
                "title": "iPhone 13 Pro - 256GB",
                "price": 799.99,
                "currency": "USD",
                "quantity": 1,
                "sku": "DEMO-PHONE-001",
                "description": "Like new iPhone 13 Pro, unlocked",
                "category": "Electronics",
                "brand": "Apple",
                "condition": "like new",
                "merchant": "Depop",
                "in_stock": True
            },
            {
                "title": "Vintage Levi's Denim Jacket",
                "price": 85.00,
                "currency": "USD",
                "quantity": 1,
                "sku": "DEMO-JACKET-001",
                "description": "Classic Levi's trucker jacket from the 90s",
                "category": "Clothing",
                "brand": "Levi's",
                "condition": "good",
                "merchant": "Depop",
                "in_stock": True
            }
        ]
        
        created_ids = []
        for item in items:
            print_info(f"Creating item: {item['title']}")
            response = requests.post(
                f"{self.base_url}/inventory",
                json=item,
                headers=self.headers
            )
            
            if response.status_code == 201:
                item_id = response.json()['item']['id']
                created_ids.append(item_id)
                print_success(f"Created item ID: {item_id}")
            else:
                print_response(response)
        
        return created_ids
    
    def demo_list_inventory(self):
        """Demo: List inventory with filters."""
        print_header("6. List Inventory Items")
        
        print_info("Fetching all inventory items...")
        response = requests.get(
            f"{self.base_url}/inventory?page=1&per_page=10",
            headers=self.headers
        )
        
        print_response(response)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Retrieved {len(data['items'])} items")
            print_info(f"Total items: {data['pagination']['total_items']}")
    
    def demo_search_inventory(self):
        """Demo: Search inventory."""
        print_header("7. Search Inventory")
        
        print_info("Searching for 'vintage' items...")
        response = requests.get(
            f"{self.base_url}/inventory?search=vintage",
            headers=self.headers
        )
        
        print_response(response)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Found {len(data['items'])} vintage items")
    
    def demo_filter_inventory(self):
        """Demo: Filter inventory by merchant."""
        print_header("8. Filter Inventory by Merchant")
        
        print_info("Filtering by merchant: Depop")
        response = requests.get(
            f"{self.base_url}/inventory?merchant=Depop",
            headers=self.headers
        )
        
        print_response(response)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Found {len(data['items'])} Depop items")
    
    def demo_update_item(self, item_id):
        """Demo: Update inventory item."""
        print_header("9. Update Inventory Item")
        
        print_info(f"Updating item {item_id}...")
        update_data = {
            "price": 89.99,
            "quantity": 2,
            "in_stock": False
        }
        
        response = requests.put(
            f"{self.base_url}/inventory/{item_id}",
            json=update_data,
            headers=self.headers
        )
        
        print_response(response)
        
        if response.status_code == 200:
            print_success(f"Updated item {item_id}")
    
    def demo_get_stats(self):
        """Demo: Get dashboard statistics."""
        print_header("10. Dashboard Statistics")
        
        print_info("Fetching dashboard stats...")
        response = requests.get(
            f"{self.base_url}/stats",
            headers=self.headers
        )
        
        print_response(response)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Statistics retrieved!")
            print_info(f"Total Items: {data['inventory']['total_items']}")
            print_info(f"Total Value: ${data['inventory']['total_value']}")
    
    def demo_scraping_job(self):
        """Demo: Create a scraping job (simulated)."""
        print_header("11. Start Scraping Job")
        
        print_info("Note: This would normally scrape a live website.")
        print_info("For demo purposes, we'll show the request structure.")
        
        job_data = {
            "url": "https://www.mercari.com/us/item/m12345678901/",
            "merchant": "Mercari",
            "max_pages": 1
        }
        
        print(f"\n{Colors.YELLOW}Request payload:{Colors.ENDC}")
        pprint(job_data, indent=2)
        
        print_info("\nTo actually start a scraping job, uncomment the code below:")
        print(f"{Colors.CYAN}# response = requests.post(")
        print(f"#     f\"{self.base_url}/scraping/scrape\",")
        print(f"#     json=job_data,")
        print(f"#     headers=self.headers")
        print(f"# ){Colors.ENDC}")
    
    def demo_list_jobs(self):
        """Demo: List scraping jobs."""
        print_header("12. List Scraping Jobs")
        
        print_info("Fetching scraping jobs...")
        response = requests.get(
            f"{self.base_url}/scraping/jobs",
            headers=self.headers
        )
        
        print_response(response)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Found {data['pagination']['total_items']} scraping jobs")
    
    def run_all_demos(self):
        """Run all API demonstrations."""
        print(f"\n{Colors.BOLD}{Colors.BLUE}")
        print("╔════════════════════════════════════════════════════════════╗")
        print("║          Inventory Hub API - Interactive Demo             ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print(f"{Colors.ENDC}\n")
        
        try:
            # Authentication demos
            self.demo_health_check()
            time.sleep(1)
            
            self.demo_register()
            time.sleep(1)
            
            self.demo_get_current_user()
            time.sleep(1)
            
            # Inventory demos
            item_ids = self.demo_create_inventory_items()
            time.sleep(1)
            
            self.demo_list_inventory()
            time.sleep(1)
            
            self.demo_search_inventory()
            time.sleep(1)
            
            self.demo_filter_inventory()
            time.sleep(1)
            
            if item_ids:
                self.demo_update_item(item_ids[0])
                time.sleep(1)
            
            # Stats demo
            self.demo_get_stats()
            time.sleep(1)
            
            # Scraping demos
            self.demo_scraping_job()
            time.sleep(1)
            
            self.demo_list_jobs()
            
            # Success message
            print_header("Demo Complete!")
            print_success("All API endpoints demonstrated successfully!")
            print_info("\nNext steps:")
            print("  1. Import the Postman collection for interactive testing")
            print("  2. Check the backend/README.md for full API documentation")
            print("  3. Build your mobile app using these endpoints")
            
        except requests.exceptions.ConnectionError:
            print_error("\nCould not connect to the API server.")
            print_info("Please make sure the server is running:")
            print(f"  cd backend && python app.py")
        except Exception as e:
            print_error(f"\nDemo failed with error: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    demo = InventoryHubAPIDemo()
    demo.run_all_demos()
