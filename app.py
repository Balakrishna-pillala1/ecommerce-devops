
from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "ecommerce-devops-local-secret"

products = [
    {"id": 1, "name": "Laptop", "price": 55000},
    {"id": 2, "name": "Mobile Phone", "price": 25000},
    {"id": 3, "name": "Headphones", "price": 2000},
    {"id": 4, "name": "Keyboard", "price": 1500},
]

@app.route("/")
def home():
    return render_template("index.html", products=products)


@app.route("/add-to-cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    product = next(
        (p for p in products if p["id"] == product_id), None
    )

    if product is None:
        return "Product not found", 404

    cart = session.get("cart", {})
    key = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    session["cart"] = cart

    return redirect(url_for("view_cart"))


@app.route("/cart")
def view_cart():
    cart = session.get("cart", {})
    cart_items = []
    total = 0

    for product in products:
        quantity = cart.get(str(product["id"]), 0)

        if quantity > 0:
            subtotal = product["price"] * quantity
            cart_items.append({
                **product,
                "quantity": quantity,
                "subtotal": subtotal
            })
            total += subtotal

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total=total
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
