from flask import Flask, render_template, send_from_directory, request, redirect, url_for, session, flash, jsonify
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
from db_connector import db
from datetime import datetime

# טעינת המשתנים מקובץ .env
load_dotenv()

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ניווט מותאם לפי משתמש
@app.context_processor
def inject_navigation():
    if "user_id" in session:
        nav_links = [
            {"url": "/", "label": "Home"},
            {"url": "/summary", "label": "Monthly Summary"},
            {"url": "/add_transaction", "label": "Add Transaction"},
            {"url": "/logout", "label": "Logout"}
        ]
    else:
        nav_links = [
            {"url": "/", "label": "Home"},
            {"url": "/login", "label": "Login"},
            {"url": "/signup", "label": "Sign Up"},
            {"url": "/contact", "label": "Contact Us"}
        ]
    return {"nav_links": nav_links}

# דף הבית
@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

# דף Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = db.users.find_one({"email": email, "password": password})
        if user:
            session["user_id"] = str(user["_id"])
            session["user_name"] = user["name"]
            return redirect(url_for("dashboard"))
        flash("Invalid email or password. Please try again.", "error")
    return render_template("login.html")

# דף Dashboard
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    transactions = list(db.transactions.find({"user_id": session["user_id"]}))
    return render_template("dashboard.html", user_name=session.get("user_name", "User"), transactions=transactions)

# דף הצגת כל הטרנזקציות
@app.route("/all_transactions")
def all_transactions():
    if "user_id" not in session:
        return redirect(url_for("login"))
    transactions = list(db.transactions.find({"user_id": session["user_id"]}))
    return render_template("all_transactions.html", transactions=transactions)

# דף סיכום חודשי
@app.route("/summary")
def summary():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    # חישוב נתונים כוללים
    total_income = sum(t["amount"] for t in db.transactions.find({"user_id": user_id, "type": "income"}))
    total_expenses = sum(t["amount"] for t in db.transactions.find({"user_id": user_id, "type": "expense"}))
    balance = total_income - total_expenses

    # חישוב הוצאות לפי קטגוריה
    categories = {}
    for t in db.transactions.find({"user_id": user_id, "type": "expense"}):
        category = t["category"]
        amount = t["amount"]
        if category in categories:
            categories[category] += amount
        else:
            categories[category] = amount

    # המרת הנתונים לייצוג המתאים עבור הגרף
    category_labels = list(categories.keys())  # שמות קטגוריות
    category_values = list(categories.values())  # סכום ההוצאות בכל קטגוריה

    return render_template(
        "summary.html",
        total_income=total_income,
        total_expenses=total_expenses,
        balance=balance,
        categories=category_labels,
        amounts=category_values
    )


   ## return render_template("summary.html", total_income=total_income, total_expenses=total_expenses, balance=balance)

# דף Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]

        # בדיקה האם האימייל כבר קיים
        existing_user = db.users.find_one({"email": email})
        if existing_user:
            flash("This email is already registered. Please use a different email.", "error")
            print("⚠️ User already exists!")  # בדיקה בטרמינל
            return redirect(url_for("signup"))

        # אם המשתמש לא קיים, מוסיפים אותו
        db.users.insert_one({"name": name, "email": email, "password": password})
        flash("Signup successful! You can now log in.", "success")
        print("✅ User registered successfully!")  # בדיקה בטרמינל
        return redirect(url_for("login"))

    return render_template("signup.html")


# דף הוספת טרנזקציה
@app.route("/add_transaction", methods=["GET", "POST"])
def add_transaction():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        transaction_type = request.form["type"]  # income או expense
        category = request.form["category"]

        try:
            amount = float(request.form["amount"])

            # בדיקה אם הסכום שלילי - לא נאפשר את זה
            if amount < 0:
                flash("Amount must be a positive number.", "error")
                return redirect(url_for("add_transaction"))

            # אם מדובר בהוצאה, נוודא שהערך יהפוך לשלילי
            if transaction_type == "expense":
                amount = -amount

            # הכנסת הנתונים למסד הנתונים
            transaction = {
                "type": transaction_type,
                "category": category,
                "amount": amount,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user_id": session["user_id"]
            }
            db.transactions.insert_one(transaction)
            flash("Transaction added successfully!", "success")
            return redirect(url_for("dashboard"))

        except ValueError:
            flash("Invalid amount. Please enter a valid number.", "error")
            return redirect(url_for("add_transaction"))

    return render_template("add_transaction.html")


# עריכת טרנזקציה
@app.route("/edit_transaction/<transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    transaction = db.transactions.find_one({"_id": ObjectId(transaction_id), "user_id": session["user_id"]})
    if not transaction:
        flash("Transaction not found!", "error")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        updated_data = {
            "type": request.form["type"],
            "category": request.form["category"],
            "amount": float(request.form["amount"]),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        db.transactions.update_one({"_id": ObjectId(transaction_id)}, {"$set": updated_data})
        flash("Transaction updated successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("edit_transaction.html", transaction=transaction)

# מחיקת טרנזקציה
@app.route("/delete_transaction/<transaction_id>", methods=["POST"])
def delete_transaction(transaction_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    result = db.transactions.delete_one({"_id": ObjectId(transaction_id), "user_id": session["user_id"]})
    if result.deleted_count == 0:
        flash("Transaction not found or not authorized!", "error")
    else:
        flash("Transaction deleted successfully!", "success")
    return redirect(url_for("dashboard"))

# API להצגת כל הטרנזקציות בפורמט JSON
@app.route("/api/transactions", methods=["GET"])
def api_get_transactions():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    transactions = list(db.transactions.find({"user_id": session["user_id"]}, {"_id": 0}))
    return jsonify(transactions)

# API להוספת טרנזקציה חדשה דרך JSON
@app.route("/api/transactions", methods=["POST"])
def api_add_transaction():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    if not data or "type" not in data or "category" not in data or "amount" not in data:
        return jsonify({"error": "Invalid data"}), 400

    transaction = {
        "type": data["type"],
        "category": data["category"],
        "amount": float(data["amount"]),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": session["user_id"]
    }
    db.transactions.insert_one(transaction)
    return jsonify({"message": "Transaction added successfully!"}), 201

# דף Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# CSS ו-JS
@app.route('/MyCss/<path:filename>')
def serve_css(filename):
    return send_from_directory('MyCss', filename)

@app.route('/MYJS/<path:filename>')
def serve_js(filename):
    return send_from_directory('MYJS', filename)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        # הכנסת ההודעה ל-MongoDB
        db.messages.insert_one({
            "name": name,
            "email": email,
            "message": message,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        flash("Thank you for your message!", "success")
        return redirect(url_for("thank_you"))

    return render_template("contact.html")



@app.route("/thank_you")
def thank_you():
    return render_template("thank_you.html")





if __name__ == "__main__":
    app.run(debug=True)

