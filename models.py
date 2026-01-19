"""
Data models for inventory items.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, List, Dict, Any
import json


@dataclass
class InventoryItem:
    """Represents a single inventory item scraped from a merchant listing."""
    
    title: str
    price: Optional[float] = None
    currency: str = "USD"
    quantity: Optional[int] = None
    sku: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    image_url: Optional[str] = None
    product_url: Optional[str] = None
    merchant: Optional[str] = None
    condition: str = "new"
    in_stock: bool = True
    scraped_at: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Set scraped_at timestamp if not provided."""
        if self.scraped_at is None:
            self.scraped_at = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the inventory item to a dictionary."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert the inventory item to a JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InventoryItem':
        """Create an InventoryItem from a dictionary."""
        return cls(**data)


class InventoryCollection:
    """Collection of inventory items with utility methods."""
    
    def __init__(self):
        self.items: List[InventoryItem] = []
    
    def add_item(self, item: InventoryItem):
        """Add an item to the collection."""
        self.items.append(item)
    
    def add_items(self, items: List[InventoryItem]):
        """Add multiple items to the collection."""
        self.items.extend(items)
    
    def to_dict_list(self) -> List[Dict[str, Any]]:
        """Convert all items to a list of dictionaries."""
        return [item.to_dict() for item in self.items]
    
    def to_json(self) -> str:
        """Convert all items to a JSON string."""
        return json.dumps(self.to_dict_list(), indent=2)
    
    def save_to_json(self, filepath: str):
        """Save the collection to a JSON file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
    
    def save_to_csv(self, filepath: str):
        """Save the collection to a CSV file."""
        import csv
        
        if not self.items:
            return
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            # Get all possible field names
            fieldnames = list(self.items[0].to_dict().keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in self.items:
                writer.writerow(item.to_dict())
    
    def __len__(self) -> int:
        """Return the number of items in the collection."""
        return len(self.items)
    
    def __iter__(self):
        """Iterate over items in the collection."""
        return iter(self.items)
