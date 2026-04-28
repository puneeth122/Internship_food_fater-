# eta_engine.py
# ETA Engine — predicts when the guest will arrive at the restaurant
# Uses distance + average speed + traffic factor to estimate arrival time
# In production, this integrates with Google Maps Distance Matrix API

import math
import random

class ETAEngine:
    AVG_SPEED_KMPH      = 30   # average city speed (Bengaluru)
    TRAFFIC_PEAK_FACTOR = 1.4  # multiplier during peak hours (8-10am, 5-8pm)
    TRAFFIC_NORM_FACTOR = 1.0

    def __init__(self):
        print("[ETAEngine] Initialized.")

    def _haversine_distance(self, loc1, loc2):
        """
        Calculates straight-line distance (km) between two lat/lng coordinates.
        Formula: Haversine
        """
        R = 6371  # Earth radius in km
        lat1, lng1 = math.radians(loc1["lat"]), math.radians(loc1["lng"])
        lat2, lng2 = math.radians(loc2["lat"]), math.radians(loc2["lng"])

        dlat = lat2 - lat1
        dlng = lng2 - lng1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def _get_traffic_factor(self):
        """Returns a traffic multiplier. In production, fetched from Maps API."""
        # Simulated — randomly apply peak or normal
        return random.choice([self.TRAFFIC_PEAK_FACTOR, self.TRAFFIC_NORM_FACTOR])

    def predict_eta(self, guest_location, restaurant_location):
        """
        Returns estimated minutes for the guest to arrive.
        guest_location      : dict with 'lat' and 'lng'
        restaurant_location : dict with 'lat' and 'lng'
        """
        distance_km    = self._haversine_distance(guest_location, restaurant_location)
        traffic_factor = self._get_traffic_factor()
        effective_speed = self.AVG_SPEED_KMPH / traffic_factor

        eta_hours   = distance_km / effective_speed
        eta_minutes = round(eta_hours * 60)

        print(f"[ETAEngine] Distance: {distance_km:.2f} km | "
              f"Traffic factor: {traffic_factor} | ETA: {eta_minutes} min")
        return eta_minutes

    def calculate_cook_start(self, eta_minutes, cook_time_minutes):
        """
        Returns how many minutes from NOW the kitchen should start cooking,
        so the food is ready exactly when the guest arrives.
        """
        cook_start = eta_minutes - cook_time_minutes
        if cook_start < 0:
            print("[ETAEngine] Warning: Guest arriving sooner than cook time! Start immediately.")
            return 0
        return cook_start
