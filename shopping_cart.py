"""
Online Shopping Cart System
Nested data structure: List -> Dictionary -> Key-Value pairs
"""

# ---------------------------------------------------------------
# 1. Data Structure: list of dictionaries
#    ("stock" added to cover stock availability)
# ---------------------------------------------------------------
cart = [
    {
        "product_id": 101,
        "name": "Laptop",
        "category": "Electronics",
        "price": 55000,
        "quantity": 1,
        "discount": 10,      # percent
        "stock": 5
    },
    {
        "product_id": 102,
        "name": "Wireless Mouse",
        "category": "Accessories",
        "price": 800,
        "quantity": 2,
        "discount": 5,
        "stock": 20
    },
    {
        "product_id": 103,
        "name": "Keyboard",
        "category": "Accessories",
        "price": 1500,
        "quantity": 1,
        "discount": 0,
        "stock": 0
    }
]

BILL_DISCOUNT_LIMIT = 50000   # extra discount if bill exceeds this
BILL_DISCOUNT_RATE = 10       # percent


def rupee(amount):
    return f"₹{amount:,.2f}"


# ---------------------------------------------------------------
# 2. Display all products
# ---------------------------------------------------------------
def display_products(cart):
    print("\n========== ALL PRODUCTS IN CART ==========")
    print(f"{'ID':<6}{'Name':<17}{'Category':<14}{'Price':>12}{'Qty':>5}{'Disc%':>7}{'Stock':>7}")
    print("-" * 68)
    for item in cart:
        print(f"{item['product_id']:<6}{item['name']:<17}{item['category']:<14}"
              f"{item['price']:>12,}{item['quantity']:>5}{item['discount']:>7}{item['stock']:>7}")


# ---------------------------------------------------------------
# 3. Cost of each item (price x quantity, minus product discount)
# ---------------------------------------------------------------
def item_cost(item):
    gross = item["price"] * item["quantity"]
    discount_amount = gross * item["discount"] / 100
    return gross, discount_amount, gross - discount_amount


def display_item_costs(cart):
    print("\n========== COST OF EACH ITEM ==========")
    print(f"{'Name':<17}{'Gross':>14}{'Discount':>14}{'Net Cost':>14}")
    print("-" * 59)
    for item in cart:
        gross, disc, net = item_cost(item)
        print(f"{item['name']:<17}{rupee(gross):>14}{rupee(disc):>14}{rupee(net):>14}")


# ---------------------------------------------------------------
# 4. Total bill + 10% extra discount if bill > ₹50,000
# ---------------------------------------------------------------
def calculate_bill(cart):
    subtotal = sum(item_cost(item)[2] for item in cart)
    extra = subtotal * BILL_DISCOUNT_RATE / 100 if subtotal > BILL_DISCOUNT_LIMIT else 0
    return subtotal, extra, subtotal - extra


def display_bill(cart):
    subtotal, extra, final = calculate_bill(cart)
    print("\n========== TOTAL BILL ==========")
    print(f"Subtotal (after product discounts): {rupee(subtotal)}")
    if extra:
        print(f"Extra {BILL_DISCOUNT_RATE}% discount (bill > {rupee(BILL_DISCOUNT_LIMIT)}): -{rupee(extra)}")
    else:
        print("Extra discount: Not applicable")
    print(f"Final Amount Payable:               {rupee(final)}")


# ---------------------------------------------------------------
# 5. Most expensive product (by unit price)
# ---------------------------------------------------------------
def most_expensive(cart):
    item = max(cart, key=lambda p: p["price"])
    print("\n========== MOST EXPENSIVE PRODUCT ==========")
    print(f"{item['name']} ({item['category']}) - {rupee(item['price'])}")


# ---------------------------------------------------------------
# 6. Products with quantity greater than 1
# ---------------------------------------------------------------
def quantity_more_than_one(cart):
    print("\n========== PRODUCTS WITH QUANTITY > 1 ==========")
    result = [item for item in cart if item["quantity"] > 1]
    if result:
        for item in result:
            print(f"{item['name']} - Qty: {item['quantity']}")
    else:
        print("None")


# ---------------------------------------------------------------
# 7. Stock availability
# ---------------------------------------------------------------
def check_stock(cart):
    print("\n========== STOCK AVAILABILITY ==========")
    for item in cart:
        if item["stock"] == 0:
            status = "OUT OF STOCK"
        elif item["stock"] < item["quantity"]:
            status = f"Only {item['stock']} available"
        else:
            status = "In Stock"
        print(f"{item['name']:<17}: {status}")


# ---------------------------------------------------------------
# 8. Group products by category
# ---------------------------------------------------------------
def group_by_category(cart):
    print("\n========== PRODUCTS BY CATEGORY ==========")
    groups = {}
    for item in cart:
        groups.setdefault(item["category"], []).append(item["name"])
    for category, names in groups.items():
        print(f"{category}: {', '.join(names)}")


# ---------------------------------------------------------------
# 9. Add / update / remove products
# ---------------------------------------------------------------
def add_product(cart, product_id, name, category, price, quantity, discount=0, stock=10):
    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            print(f"\nUpdated quantity of {name} to {item['quantity']}")
            return
    cart.append({
        "product_id": product_id,
        "name": name,
        "category": category,
        "price": price,
        "quantity": quantity,
        "discount": discount,
        "stock": stock
    })
    print(f"\nAdded {name} to cart")


def remove_product(cart, product_id):
    for item in cart:
        if item["product_id"] == product_id:
            cart.remove(item)
            print(f"\nRemoved {item['name']} from cart")
            return
    print(f"\nProduct ID {product_id} not found")


# ---------------------------------------------------------------
# Main
# ---------------------------------------------------------------
if __name__ == "__main__":
    display_products(cart)
    display_item_costs(cart)
    display_bill(cart)
    most_expensive(cart)
    quantity_more_than_one(cart)
    check_stock(cart)
    group_by_category(cart)

    # Demo: customer adds and removes products
    print("\n\n########## CART UPDATES ##########")
    add_product(cart, 104, "USB Cable", "Accessories", 300, 3, discount=0, stock=50)
    add_product(cart, 102, "Wireless Mouse", "Accessories", 800, 1)
    remove_product(cart, 103)

    display_products(cart)
    display_bill(cart)
