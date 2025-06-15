from flask import Blueprint, request

from api.database import get_db

categories_blueprint = Blueprint("categories", __name__)


@categories_blueprint.route("/", methods=["GET"])
def list_items():
    db = get_db()
    cursor = db.execute("SELECT * FROM categories")
    return [dict(category) for category in cursor.fetchall()], 200


@categories_blueprint.route("/add", methods=["POST"])
def add():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description", "")

    db = get_db()
    db.execute(
        "INSERT INTO categories (category_name, category_description) VALUES (?, ?)",
        (name, description),
    )
    db.commit()
    return {"message": "Category added successfully"}, 201
