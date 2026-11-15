# 🛒 Online Shopping Cart (Flask)

A simple online shopping cart for an e-commerce application, built with Python and Flask. The cart is stored as a **nested data structure**: a list of dictionaries, each holding key-value pairs for one product.

```
Cart → List
 ├── Product 1 → Dictionary (product_id, name, category, price, quantity, discount, stock)
 ├── Product 2 → Dictionary
 └── Product 3 → Dictionary
```

## Features

- Display all products in the cart
- Calculate the cost of each item (price × quantity, minus product discount)
- Calculate the total bill
- Extra 10% discount when the bill exceeds ₹50,000
- Find the most expensive product
- Show products with quantity greater than 1
- Stock availability check (In Stock / Low / Out of Stock)
- Group products by category
- Add, update quantity, and remove products from the web page

## Files

| File | Description |
|---|---|
| `app.py` | Flask web app |
| `shopping_cart.py` | Console version of the same program |
| `requirements.txt` | Python dependencies |

## How to Run

```bash
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

To run the console version:

```bash
python shopping_cart.py
```

## Sample Output

| Product | Price | Qty | Discount | Net Cost |
|---|---|---|---|---|
| Laptop | ₹55,000 | 1 | 10% | ₹49,500 |
| Wireless Mouse | ₹800 | 2 | 5% | ₹1,520 |
| Keyboard | ₹1,500 | 1 | 0% | ₹1,500 |

- Subtotal: ₹52,520
- Extra 10% discount: −₹5,252
- **Final amount: ₹47,268**

## Tech Stack

Python · Flask · HTML · CSS
