import random
import time
import threading
import json

class PricePublisher:
    def __init__(self):
        self.subscribers = []
        self.price_data = {
            "FNGU": 100.00, 
            "FNGD": 100.00 
        }
    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)
    def unsubscribe(self, subscriber):
        self.subscribers.remove(subscriber)
    def notify_subscribers(self):
        for subscriber in self.subscribers:
            subscriber.update(self.price_data)
    def simulate_price_changes(self):
        while True:
            symbol = random.choice(["FNGU", "FNGD"])
            change = random.uniform(-5.0, 5.0)
            new_price = round(self.price_data[symbol] + change, 2)
            self.price_data[symbol] = new_price
            print(f"Price updated: {symbol} -> {new_price}")
            self.notify_subscribers()
            time.sleep(1)
class PriceSubscriber:
    def __init__(self, name):
        self.name = name
    def update(self, price_data):
        fngu_price = price_data.get("FNGU")
        fngd_price = price_data.get("FNGD")
        print(f"{self.name} received update: FNGU: ${fngu_price}, FNGD: ${fngd_price}")
def main():
    publisher = PricePublisher()
    subscriber1 = PriceSubscriber("Subscriber 1")
    subscriber2 = PriceSubscriber("Subscriber 2")
    publisher.subscribe(subscriber1)
    publisher.subscribe(subscriber2)
    price_update_thread = threading.Thread(target=publisher.simulate_price_changes)
    price_update_thread.daemon = True
    price_update_thread.start()
    time.sleep(10)
    publisher.unsubscribe(subscriber1)
    publisher.unsubscribe(subscriber2)
    print("Unsubscribed all subscribers, ending simulation.")

if __name__ == "__main__":
    main()