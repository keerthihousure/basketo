"""
Basketo — Sample Data Generator
Generates realistic grocery shopping platform data for dashboard
"""

import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

# ── Config ─────────────────────────────────────────────────
START_DATE = datetime(2024, 9, 1)
END_DATE   = datetime(2024, 11, 30)
N_USERS    = 200
N_SESSIONS = 1000

CATEGORIES = ["Fruits & Veg", "Dairy", "Bakery", "Meat & Seafood",
               "Snacks", "Beverages", "Frozen", "Household"]

PRODUCTS = {
    "Fruits & Veg" : ["Bananas", "Apples", "Spinach", "Tomatoes", "Carrots"],
    "Dairy"        : ["Whole Milk", "Greek Yogurt", "Cheddar Cheese", "Butter", "Eggs"],
    "Bakery"       : ["Sourdough Bread", "Croissants", "Bagels", "Muffins"],
    "Meat & Seafood": ["Chicken Breast", "Salmon Fillet", "Ground Beef", "Shrimp"],
    "Snacks"       : ["Chips", "Granola Bar", "Popcorn", "Mixed Nuts"],
    "Beverages"    : ["Orange Juice", "Sparkling Water", "Coffee", "Green Tea"],
    "Frozen"       : ["Frozen Pizza", "Ice Cream", "Frozen Peas", "Waffles"],
    "Household"    : ["Dish Soap", "Paper Towels", "Laundry Detergent", "Sponges"]
}

FUNNEL_STAGES = ["Landing", "Browse", "Product View", "Add to Cart",
                 "Checkout Start", "Payment", "Order Confirmed"]

DROP_RATES = [0.0, 0.10, 0.15, 0.20, 0.25, 0.15, 0.05]

DEVICES     = ["Mobile", "Desktop", "Tablet"]
DEVICE_W    = [0.60, 0.30, 0.10]
DELIVERY_WINDOWS = ["8AM-12PM", "12PM-4PM", "4PM-8PM", "8PM-10PM"]


def random_date():
    delta = END_DATE - START_DATE
    return START_DATE + timedelta(days=random.randint(0, delta.days))


# ── 1. USER SESSIONS ───────────────────────────────────────
sessions = []
for i in range(N_SESSIONS):
    user_id   = f"U{random.randint(1, N_USERS):04d}"
    session_id = f"S{i+1:05d}"
    date      = random_date()
    device    = random.choices(DEVICES, weights=DEVICE_W)[0]
    duration  = random.randint(2, 45)
    pages     = random.randint(1, 18)

    # Funnel drop-off
    reached_stage = "Landing"
    for j, stage in enumerate(FUNNEL_STAGES):
        if random.random() < DROP_RATES[j]:
            break
        reached_stage = stage

    converted = 1 if reached_stage == "Order Confirmed" else 0

    sessions.append({
        "session_id"    : session_id,
        "user_id"       : user_id,
        "date"          : date.strftime("%Y-%m-%d"),
        "device"        : device,
        "duration_mins" : duration,
        "pages_viewed"  : pages,
        "last_stage"    : reached_stage,
        "converted"     : converted
    })

sessions_df = pd.DataFrame(sessions)
sessions_df.to_csv("data/user_sessions.csv", index=False)
print(f"Generated {len(sessions_df)} session records")


# ── 2. PURCHASE ORDERS ─────────────────────────────────────
orders = []
order_items = []
order_id_counter = 1

for _, session in sessions_df[sessions_df["converted"] == 1].iterrows():
    order_id = f"ORD{order_id_counter:05d}"
    n_items  = random.randint(2, 12)
    category = random.choice(CATEGORIES)
    subtotal = round(random.uniform(18, 140), 2)
    delivery = random.choice(DELIVERY_WINDOWS)
    delivery_date = (datetime.strptime(session["date"], "%Y-%m-%d")
                     + timedelta(days=random.randint(1, 3))).strftime("%Y-%m-%d")

    on_time  = 1 if random.random() < 0.82 else 0
    delay_mins = 0 if on_time else random.randint(15, 120)

    orders.append({
        "order_id"       : order_id,
        "session_id"     : session["session_id"],
        "user_id"        : session["user_id"],
        "order_date"     : session["date"],
        "delivery_date"  : delivery_date,
        "delivery_window": delivery,
        "on_time"        : on_time,
        "delay_mins"     : delay_mins,
        "n_items"        : n_items,
        "subtotal_usd"   : subtotal,
        "device"         : session["device"]
    })

    for _ in range(n_items):
        cat     = random.choice(CATEGORIES)
        product = random.choice(PRODUCTS[cat])
        qty     = random.randint(1, 4)
        price   = round(random.uniform(1.5, 18.0), 2)
        order_items.append({
            "order_id"  : order_id,
            "category"  : cat,
            "product"   : product,
            "quantity"  : qty,
            "unit_price": price,
            "line_total": round(qty * price, 2)
        })

    order_id_counter += 1

orders_df = pd.DataFrame(orders)
items_df  = pd.DataFrame(order_items)
orders_df.to_csv("data/orders.csv", index=False)
items_df.to_csv("data/order_items.csv", index=False)
print(f"Generated {len(orders_df)} orders and {len(items_df)} order items")


# ── 3. FUNNEL DATA ─────────────────────────────────────────
funnel_counts = sessions_df["last_stage"].value_counts()
funnel_data = []
for stage in FUNNEL_STAGES:
    count = int(sessions_df[
        sessions_df["last_stage"].apply(
            lambda x: FUNNEL_STAGES.index(x) >= FUNNEL_STAGES.index(stage)
            if x in FUNNEL_STAGES else False
        )
    ].shape[0])
    funnel_data.append({"stage": stage, "users": count})

funnel_df = pd.DataFrame(funnel_data)
funnel_df.to_csv("data/funnel.csv", index=False)
print(f"Generated funnel data across {len(FUNNEL_STAGES)} stages")

print("\nAll data files saved to /data/")
