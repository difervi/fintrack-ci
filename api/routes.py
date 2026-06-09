from flask import Blueprint, jsonify, request
from models import db, User, Category, Transaction

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/users", methods=["POST"])
def create_user():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "name and email are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "email already registered"}), 409

    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@api.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


@api.route("/categories", methods=["GET"])
def list_categories():
    categories = Category.query.order_by(Category.name).all()
    return jsonify([c.to_dict() for c in categories])


@api.route("/categories", methods=["POST"])
def create_category():
    data = request.get_json() or {}
    name = data.get("name")

    if not name:
        return jsonify({"error": "name is required"}), 400

    if Category.query.filter_by(name=name).first():
        return jsonify({"error": "category already exists"}), 409

    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict()), 201


@api.route("/transactions", methods=["POST"])
def create_transaction():
    data = request.get_json() or {}

    required = ["user_id", "category_id", "type", "amount"]
    missing = [field for field in required if field not in data]
    if missing:
        return jsonify({"error": f"missing fields: {', '.join(missing)}"}), 400

    if data["type"] not in ("income", "expense"):
        return jsonify({"error": "type must be 'income' or 'expense'"}), 400

    transaction = Transaction(
        user_id=data["user_id"],
        category_id=data["category_id"],
        type=data["type"],
        amount=data["amount"],
        description=data.get("description"),
    )
    db.session.add(transaction)
    db.session.commit()
    return jsonify(transaction.to_dict()), 201


@api.route("/transactions", methods=["GET"])
def list_transactions():
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        return jsonify({"error": "user_id query parameter is required"}), 400

    transactions = (
        Transaction.query.filter_by(user_id=user_id)
        .order_by(Transaction.date.desc())
        .all()
    )
    return jsonify([t.to_dict() for t in transactions])


@api.route("/transactions/summary", methods=["GET"])
def transaction_summary():
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        return jsonify({"error": "user_id query parameter is required"}), 400

    transactions = Transaction.query.filter_by(user_id=user_id).all()
    income = sum(float(t.amount) for t in transactions if t.type == "income")
    expense = sum(float(t.amount) for t in transactions if t.type == "expense")

    return jsonify(
        {
            "user_id": user_id,
            "total_income": round(income, 2),
            "total_expense": round(expense, 2),
            "balance": round(income - expense, 2),
            "transaction_count": len(transactions),
        }
    )


@api.route("/transactions/<int:transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    db.session.delete(transaction)
    db.session.commit()
    return jsonify({"message": "transaction deleted", "id": transaction_id})