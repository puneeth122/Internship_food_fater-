# cook_time.py
# Cook-Time Engine — predicts the total time needed to cook all items in an order
# Considers parallel cooking, kitchen load, and dish-specific cook times

from order import Order

class CookTimeEngine:
    KITCHEN_LOAD_FACTOR = {
        "low":    1.0,   # < 3 active orders
        "medium": 1.2,   # 3–6 active orders
        "high":   1.5,   # > 6 active orders
    }

    def __init__(self):
        self.active_orders = 0  # tracks current kitchen load
        print("[CookTimeEngine] Initialized.")

    def _get_load_factor(self):
        if self.active_orders < 3:
            return self.KITCHEN_LOAD_FACTOR["low"]
        elif self.active_orders <= 6:
            return self.KITCHEN_LOAD_FACTOR["medium"]
        else:
            return self.KITCHEN_LOAD_FACTOR["high"]

    def predict_cook_time(self, items):
        """
        Predicts total cook time (minutes) for a list of dishes.
        Assumes parallel cooking — total time = max dish time (bottleneck),
        adjusted by kitchen load factor.
        items : list of dish name strings
        """
        dummy_order = Order(guest_name="dummy", items=items)
        dish_times  = [dummy_order.get_item_cook_time(item) for item in items]

        if not dish_times:
            return 0

        # Parallel cooking: bottleneck = longest dish
        base_cook_time  = max(dish_times)
        load_factor     = self._get_load_factor()
        adjusted_time   = round(base_cook_time * load_factor)

        print(f"[CookTimeEngine] Items: {items}")
        print(f"[CookTimeEngine] Dish times: {dish_times} | "
              f"Load factor: {load_factor} | Cook time: {adjusted_time} min")
        return adjusted_time

    def register_order(self):
        """Call when a new order enters the kitchen."""
        self.active_orders += 1

    def complete_order(self):
        """Call when an order is served."""
        if self.active_orders > 0:
            self.active_orders -= 1

    def get_kitchen_load(self):
        if self.active_orders < 3:
            return "low"
        elif self.active_orders <= 6:
            return "medium"
        return "high"
