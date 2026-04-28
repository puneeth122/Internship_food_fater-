# restaurant.py
# Manages restaurant data, tables, and their availability status

from datetime import datetime

class Table:
    STATUS_AVAILABLE = "available"
    STATUS_OCCUPIED = "occupied"
    STATUS_RESERVED = "reserved"

    def __init__(self, table_id, capacity=4):
        self.table_id = table_id
        self.capacity = capacity
        self.status = self.STATUS_AVAILABLE
        self.occupied_since = None
        self.estimated_free_at = None  # filled by TableForecast

    def occupy(self):
        self.status = self.STATUS_OCCUPIED
        self.occupied_since = datetime.now()

    def release(self):
        self.status = self.STATUS_AVAILABLE
        self.occupied_since = None
        self.estimated_free_at = None

    def reserve(self, free_at_minutes):
        self.status = self.STATUS_RESERVED
        self.estimated_free_at = free_at_minutes

    def is_available(self):
        return self.status == self.STATUS_AVAILABLE

    def __repr__(self):
        return f"Table(id={self.table_id}, status={self.status}, capacity={self.capacity})"


class Restaurant:
    def __init__(self, name, total_tables=10):
        self.name = name
        self.tables = {
            f"T{i}": Table(table_id=f"T{i}", capacity=4 if i % 2 == 0 else 2)
            for i in range(1, total_tables + 1)
        }
        print(f"[Restaurant] '{self.name}' initialized with {total_tables} tables.")

    def get_all_tables(self):
        return list(self.tables.values())

    def get_available_tables(self):
        return [t for t in self.tables.values() if t.is_available()]

    def get_table_by_id(self, table_id):
        return self.tables.get(table_id, None)

    def get_table_status_summary(self):
        summary = {}
        for tid, table in self.tables.items():
            summary[tid] = table.status
        return summary

    def __repr__(self):
        available = len(self.get_available_tables())
        return f"Restaurant(name={self.name}, available_tables={available}/{len(self.tables)})"
