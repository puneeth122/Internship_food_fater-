# order.py
# Represents a guest's order — used across all engines and notification services

import uuid
from datetime import datetime

class Order:
    STATUS_PENDING   = "pending"
    STATUS_COOKING   = "cooking"
    STATUS_READY     = "ready"
    STATUS_SERVED    = "served"

    # Average cook time per dish in minutes (used by CookTimeEngine)
    DISH_COOK_TIMES = {
        "Chicken Tikka Masala": 15,
        "Paneer Butter Masala": 12,
        "Naan x2":              5,
        "Biryani":             20,
        "Lassi":                3,
        "Dosa":                 8,
        "Idli":                 6,
        "Tandoori Chicken":    18,
        "Fried Rice":          10,
        "Default":              10,  # fallback for unknown items
    }

    def __init__(self, guest_name, items, table_id=None):
        self.order_id   = str(uuid.uuid4())[:8].upper()
        self.guest_name = guest_name
        self.items      = items
        self.table_id   = table_id
        self.status     = self.STATUS_PENDING
        self.placed_at  = datetime.now()

    def get_item_cook_time(self, item):
        return self.DISH_COOK_TIMES.get(item, self.DISH_COOK_TIMES["Default"])

    def update_status(self, new_status):
        valid = [self.STATUS_PENDING, self.STATUS_COOKING,
                 self.STATUS_READY, self.STATUS_SERVED]
        if new_status not in valid:
            raise ValueError(f"Invalid status: {new_status}")
        self.status = new_status
        print(f"[Order {self.order_id}] Status updated → {new_status}")

    def summary(self):
        return {
            "order_id":   self.order_id,
            "guest":      self.guest_name,
            "items":      self.items,
            "table":      self.table_id,
            "status":     self.status,
            "placed_at":  self.placed_at.strftime("%H:%M:%S"),
        }

    def __repr__(self):
        return (f"Order(id={self.order_id}, guest={self.guest_name}, "
                f"items={self.items}, status={self.status})")
