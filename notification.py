# notification.py
# Notification Service — sends alerts to the Kitchen Display System (KDS)
# and the Waiter App at the right moment (the Perfect Serve Moment)

from datetime import datetime, timedelta
from order import Order

class NotificationService:

    def __init__(self):
        self.log = []  # stores all sent notifications
        print("[NotificationService] Initialized.")

    def _send(self, recipient, message, order_id):
        timestamp = datetime.now().strftime("%H:%M:%S")
        notification = {
            "timestamp":  timestamp,
            "recipient":  recipient,
            "order_id":   order_id,
            "message":    message,
        }
        self.log.append(notification)
        print(f"[{timestamp}] NOTIFY → {recipient}: {message}")

    def notify_kitchen(self, order: Order, cook_start_in_minutes):
        """
        Tells the KDS (Kitchen Display System) when to start cooking.
        cook_start_in_minutes : delay before kitchen starts
        """
        start_time = datetime.now() + timedelta(minutes=cook_start_in_minutes)
        start_str  = start_time.strftime("%H:%M")

        items_str = ", ".join(order.items)
        message = (
            f"[KDS] Order #{order.order_id} | Guest: {order.guest_name} | "
            f"Table: {order.table_id} | Items: {items_str} | "
            f"START COOKING AT: {start_str}"
        )
        self._send(recipient="Kitchen Display System", message=message,
                   order_id=order.order_id)
        order.update_status(Order.STATUS_COOKING)

    def notify_waiter(self, order: Order, eta_minutes):
        """
        Alerts the Waiter App to be ready to serve when the guest arrives.
        """
        arrival_time = datetime.now() + timedelta(minutes=eta_minutes)
        arrival_str  = arrival_time.strftime("%H:%M")

        message = (
            f"[WAITER] Order #{order.order_id} | Guest: {order.guest_name} | "
            f"Table: {order.table_id} | "
            f"Food will be ready at arrival: {arrival_str}. Be at the table!"
        )
        self._send(recipient="Waiter App", message=message,
                   order_id=order.order_id)

    def notify_host(self, table_id, guest_name, eta_minutes):
        """
        Alerts the Host Console about incoming guest and table assignment.
        """
        message = (
            f"[HOST] Incoming guest: {guest_name} | "
            f"ETA: {eta_minutes} min | Table assigned: {table_id}"
        )
        self._send(recipient="Host Console", message=message,
                   order_id="N/A")

    def get_notification_log(self):
        """Returns all notifications sent in this session."""
        return self.log
