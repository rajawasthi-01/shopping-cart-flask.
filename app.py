"""
Online Shopping Cart - Flask App
Run:  pip install flask
      python app.py
Open: http://127.0.0.1:5000
"""

from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

BILL_DISCOUNT_LIMIT = 50000
BILL_DISCOUNT_RATE = 10

# Nested data structure: List -> Dictionary -> Key-Value pairs
cart = [
    {"product_id": 101, "name": "Laptop", "category": "Electronics",
     "price": 55000, "quantity": 1, "discount": 10, "stock": 5},
    {"product_id": 102, "name": "Wireless Mouse", "category": "Accessories",
     "price": 800, "quantity": 2, "discount": 5, "stock": 20},
    {"product_id": 103, "name": "Keyboard", "category": "Accessories",
     "price": 1500, "quantity": 1, "discount": 0, "stock": 0},
]


# ---------------- Cart logic ----------------
def item_cost(item):
    gross = item["price"] * item["quantity"]
    disc = gross * item["discount"] / 100
    return gross, disc, gross - disc


def stock_status(item):
    if item["stock"] == 0:
        return "Out of Stock", "out"
    if item["stock"] < item["quantity"]:
        return f"Only {item['stock']} left", "low"
    return "In Stock", "in"


def calculate_bill():
    subtotal = sum(item_cost(i)[2] for i in cart)
    extra = subtotal * BILL_DISCOUNT_RATE / 100 if subtotal > BILL_DISCOUNT_LIMIT else 0
    return subtotal, extra, subtotal - extra


def find_item(pid):
    return next((i for i in cart if i["product_id"] == pid), None)


# ---------------- Routes ----------------
@app.route("/")
def index():
    rows = []
    for item in cart:
        gross, disc, net = item_cost(item)
        status, css = stock_status(item)
        rows.append({**item, "gross": gross, "disc_amt": disc, "net": net,
                     "status": status, "css": css})

    subtotal, extra, final = calculate_bill()
    most_expensive = max(cart, key=lambda i: i["price"]) if cart else None
    multi_qty = [i for i in cart if i["quantity"] > 1]

    categories = {}
    for i in cart:
        categories.setdefault(i["category"], []).append(i["name"])

    return render_template_string(
        TEMPLATE, rows=rows, subtotal=subtotal, extra=extra, final=final,
        most_expensive=most_expensive, multi_qty=multi_qty,
        categories=categories, limit=BILL_DISCOUNT_LIMIT, rate=BILL_DISCOUNT_RATE,
        message=request.args.get("msg"))


@app.route("/add", methods=["POST"])
def add():
    f = request.form
    try:
        pid = int(f["product_id"])
        qty = int(f["quantity"])
        existing = find_item(pid)
        if existing:
            existing["quantity"] += qty
            msg = f"Updated {existing['name']} quantity to {existing['quantity']}"
        else:
            cart.append({
                "product_id": pid,
                "name": f["name"].strip(),
                "category": f["category"].strip(),
                "price": float(f["price"]),
                "quantity": qty,
                "discount": float(f.get("discount") or 0),
                "stock": int(f.get("stock") or 0),
            })
            msg = f"Added {f['name'].strip()} to cart"
    except (ValueError, KeyError):
        msg = "Invalid input - please check the form"
    return redirect(url_for("index", msg=msg))


@app.route("/update/<int:pid>", methods=["POST"])
def update(pid):
    item = find_item(pid)
    if item:
        qty = int(request.form.get("quantity", item["quantity"]))
        if qty <= 0:
            cart.remove(item)
            return redirect(url_for("index", msg=f"Removed {item['name']}"))
        item["quantity"] = qty
    return redirect(url_for("index", msg="Quantity updated"))


@app.route("/remove/<int:pid>", methods=["POST"])
def remove(pid):
    item = find_item(pid)
    if item:
        cart.remove(item)
        return redirect(url_for("index", msg=f"Removed {item['name']}"))
    return redirect(url_for("index"))


# ---------------- HTML Template ----------------
TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Online Shopping Cart</title>
<style>
  * { box-sizing: border-box; }
  body { font-family: system-ui, Arial, sans-serif; background:#f4f6f9; margin:0; padding:30px; color:#222; }
  .wrap { max-width: 1000px; margin:auto; }
  h1 { text-align:center; color:#2c3e50; }
  .card { background:#fff; border-radius:10px; padding:20px 24px; margin-bottom:20px; box-shadow:0 2px 8px rgba(0,0,0,.08); }
  h2 { margin-top:0; font-size:1.1rem; color:#34495e; border-bottom:2px solid #eef1f5; padding-bottom:8px; }
  table { width:100%; border-collapse:collapse; font-size:.92rem; }
  th, td { padding:9px; border-bottom:1px solid #eee; text-align:left; }
  th { background:#2c3e50; color:#fff; }
  .num { text-align:right; }
  .in { color:#27ae60; font-weight:600; } .low { color:#e67e22; font-weight:600; } .out { color:#c0392b; font-weight:600; }
  .grid { display:grid; grid-template-columns:1fr 1fr; gap:20px; }
  .row { display:flex; justify-content:space-between; padding:5px 0; }
  .total { font-weight:bold; font-size:1.15rem; border-top:2px solid #2c3e50; margin-top:6px; padding-top:10px; }
  .green { color:#27ae60; }
  .msg { background:#e8f6ef; border-left:4px solid #27ae60; padding:10px 14px; border-radius:4px; margin-bottom:20px; }
  form.inline { display:inline; }
  input { padding:7px; border:1px solid #ccc; border-radius:5px; }
  input.qty { width:55px; }
  button { padding:7px 12px; border:none; border-radius:5px; cursor:pointer; background:#2c3e50; color:#fff; }
  button.del { background:#c0392b; }
  .addform { display:grid; grid-template-columns:repeat(4,1fr); gap:10px; }
  .addform button { grid-column: span 4; padding:10px; }
  ul { margin:0; padding-left:20px; }
</style>
</head>
<body>
<div class="wrap">
  <h1>🛒 Online Shopping Cart</h1>
  {% if message %}<div class="msg">{{ message }}</div>{% endif %}

  <div class="card">
    <h2>Products in Cart</h2>
    <table>
      <tr>
        <th>ID</th><th>Name</th><th>Category</th><th class="num">Price</th>
        <th>Qty</th><th class="num">Disc %</th><th class="num">Net Cost</th>
        <th>Stock</th><th></th>
      </tr>
      {% for r in rows %}
      <tr>
        <td>{{ r.product_id }}</td>
        <td>{{ r.name }}</td>
        <td>{{ r.category }}</td>
        <td class="num">₹{{ "{:,.0f}".format(r.price) }}</td>
        <td>
          <form class="inline" method="post" action="/update/{{ r.product_id }}">
            <input class="qty" type="number" name="quantity" value="{{ r.quantity }}" min="0">
            <button>✓</button>
          </form>
        </td>
        <td class="num">{{ "{:g}".format(r.discount) }}%</td>
        <td class="num">₹{{ "{:,.2f}".format(r.net) }}</td>
        <td class="{{ r.css }}">{{ r.status }}</td>
        <td>
          <form class="inline" method="post" action="/remove/{{ r.product_id }}">
            <button class="del">Remove</button>
          </form>
        </td>
      </tr>
      {% else %}
      <tr><td colspan="9">Cart is empty</td></tr>
      {% endfor %}
    </table>
  </div>

  <div class="grid">
    <div class="card">
      <h2>Total Bill</h2>
      <div class="row"><span>Subtotal (after product discounts)</span><span>₹{{ "{:,.2f}".format(subtotal) }}</span></div>
      <div class="row green">
        <span>Extra {{ rate }}% off {% if not extra %}(bill must exceed ₹{{ "{:,}".format(limit) }}){% endif %}</span>
        <span>- ₹{{ "{:,.2f}".format(extra) }}</span>
      </div>
      <div class="row total"><span>Amount Payable</span><span>₹{{ "{:,.2f}".format(final) }}</span></div>
    </div>

    <div class="card">
      <h2>Cart Insights</h2>
      <p><b>Most expensive:</b>
        {% if most_expensive %}{{ most_expensive.name }} (₹{{ "{:,.0f}".format(most_expensive.price) }}){% else %}-{% endif %}</p>
      <p><b>Quantity greater than 1:</b>
        {% if multi_qty %}{{ multi_qty | map(attribute='name') | join(', ') }}{% else %}None{% endif %}</p>
      <p><b>By category:</b></p>
      <ul>
        {% for cat, names in categories.items() %}<li>{{ cat }}: {{ names | join(', ') }}</li>{% endfor %}
      </ul>
    </div>
  </div>

  <div class="card">
    <h2>Add Product</h2>
    <form class="addform" method="post" action="/add">
      <input name="product_id" type="number" placeholder="Product ID" required>
      <input name="name" placeholder="Name" required>
      <input name="category" placeholder="Category" required>
      <input name="price" type="number" step="0.01" placeholder="Price" required>
      <input name="quantity" type="number" min="1" placeholder="Quantity" required>
      <input name="discount" type="number" step="0.01" placeholder="Discount %">
      <input name="stock" type="number" min="0" placeholder="Stock">
      <span></span>
      <button>Add to Cart</button>
    </form>
    <p style="font-size:.85rem;color:#777">Using an existing Product ID adds to that product's quantity.</p>
  </div>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)
