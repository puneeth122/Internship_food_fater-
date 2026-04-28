# main.py
# Food Faster - Time Intelligence Platform for Restaurants
# Prinfio Tech Pvt Ltd | Founder: Prasanth

from restaurant import Restaurant
from order import Order
from eta_engine import ETAEngine
from cook_time import CookTimeEngine
from table_forecast import TableForecast
from notification import NotificationService

def main():
    print("=" * 50)
    print("   Food Faster - Time Intelligence Platform")
    print("=" * 50)

    # Initialize restaurant
    restaurant = Restaurant(name="Spice Garden", total_tables=10)

    # Initialize engines
    eta_engine = ETAEngine()
    cook_engine = CookTimeEngine()
    table_forecast = TableForecast(restaurant)
    notifier = NotificationService()

    # Simulate a guest placing an order
    guest_location = {"lat": 12.9716, "lng": 77.5946}  # Bengaluru
    restaurant_location = {"lat": 12.9352, "lng": 77.6245}

    # Step 1: Predict guest ETA
    eta_minutes = eta_engine.predict_eta(guest_location, restaurant_location)
    print(f"\n[ETA Engine] Guest will arrive in: {eta_minutes} minutes")

    # Step 2: Create order
    order = Order(
        guest_name="Raakesh",
        items=["Chicken Tikka Masala", "Naan x2", "Lassi"],
        table_id=None
    )

    # Step 3: Predict cook time for the order
    cook_time = cook_engine.predict_cook_time(order.items)
    print(f"[Cook Engine] Estimated cook time: {cook_time} minutes")

    # Step 4: Forecast table availability
    available_table = table_forecast.get_available_table(eta_minutes)
    order.table_id = available_table
    print(f"[Table Forecast] Table assigned: {available_table}")

    # Step 5: Calculate perfect serve moment
    cook_start_time = eta_engine.calculate_cook_start(eta_minutes, cook_time)
    print(f"[Perfect Serve] Kitchen should start cooking in: {cook_start_time} minutes")

    # Step 6: Notify kitchen and waiter
    notifier.notify_kitchen(order, cook_start_time)
    notifier.notify_waiter(order, eta_minutes)

    print("\n[Food Faster] Perfect Serve Moment synchronized successfully!")
    print("=" * 50)

if __name__ == "__main__":
    main()
