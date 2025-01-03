from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Expense
from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = SECRET_KEY
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

# Home page - List all expenses
@app.route("/")
def index():
    expenses = Expense.query.all()
    return render_template("index.html", expenses=expenses)

# Add a new expense
@app.route("/add", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        description = request.form["description"]
        amount = float(request.form["amount"])
        category = request.form["category"]

        new_expense = Expense(description=description, amount=amount, category=category)
        db.session.add(new_expense)
        db.session.commit()
        flash("Expense added successfully!", "success")
        return redirect(url_for("index"))
    return render_template("add_expense.html")

# Edit an expense
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_expense(id):
    expense = Expense.query.get_or_404(id)
    if request.method == "POST":
        expense.description = request.form["description"]
        expense.amount = float(request.form["amount"])
        expense.category = request.form["category"]
        db.session.commit()
        flash("Expense updated successfully!", "success")
        return redirect(url_for("index"))
    return render_template("edit_expense.html", expense=expense)

# Delete an expense
@app.route("/delete/<int:id>")
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted successfully!", "danger")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
