# table_forecast.py
# Table Forecast Engine — predicts which table will be free by the time the guest arrives
# Uses average dining duration to estimate table turnover time

import random
from restaurant import Restaurant

class TableForecast:
    AVG_DINING_DURATION = 45  # average minutes a guest occupies a table

    def __init__(self, restaurant: Restaurant):
        self.restaurant = restaurant
        self._simulate_occupied_tables()
        print("[TableForecast] Initialized with restaurant table data.")

    def _simulate_occupied_tables(self):
        """
        Simulates some tables being already occupied with random time remaining.
        In production, this comes from live POS/KDS data.
        """
        tables = self.restaurant.get_all_tables()
        for i, table in enumerate(tables):
            if i % 3 == 0:  # occupy every 3rd table
                time_remaining = random.randint(5, 40)
                table.occupy()
                table.estimated_free_at = time_remaining
                print(f"[TableForecast] {table.table_id} occupied, "
                      f"free in ~{time_remaining} min")

    def get_available_table(self, guest_eta_minutes):
        """
        Returns the best table ID that will be available when the guest arrives.
        Priority: already free > freeing up before ETA > any table
        guest_eta_minutes : int, minutes until guest arrives
        """
        tables = self.restaurant.get_all_tables()

        # Priority 1: already available tables
        free_tables = [t for t in tables if t.is_available()]
        if free_tables:
            chosen = free_tables[0]
            print(f"[TableForecast] Table {chosen.table_id} is already available.")
            return chosen.table_id

        # Priority 2: tables that will free up before guest arrives
        freeing_soon = [
            t for t in tables
            if t.estimated_free_at is not None and t.estimated_free_at <= guest_eta_minutes
        ]
        if freeing_soon:
            chosen = min(freeing_soon, key=lambda t: t.estimated_free_at)
            chosen.reserve(guest_eta_minutes)
            print(f"[TableForecast] Table {chosen.table_id} will free in "
                  f"{chosen.estimated_free_at} min — reserved for guest.")
            return chosen.table_id

        # Fallback: assign any table (host will manage manually)
        fallback = tables[0]
        print(f"[TableForecast] No ideal table found. Assigning {fallback.table_id} as fallback.")
        return fallback.table_id

    def get_forecast_summary(self):
        """Returns a summary of all tables and their estimated availability."""
        summary = []
        for table in self.restaurant.get_all_tables():
            summary.append({
                "table_id":       table.table_id,
                "status":         table.status,
                "free_in_minutes": table.estimated_free_at,
            })
        return summary
