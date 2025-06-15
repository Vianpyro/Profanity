from flask import Blueprint, request

from api.database import get_db

profanities_blueprint = Blueprint("profanities", __name__)


@profanities_blueprint.route("/", methods=["GET"])
def list_items():
    db = get_db()
    cursor = db.execute("SELECT * FROM profanities")
    return [dict(profanity) for profanity in cursor.fetchall()], 200


@profanities_blueprint.route("/add", methods=["POST"])
def add():
    data = request.get_json()
    profanity = data.get("profanity")
    language = data.get("language")
    category = data.get("category", None)
    severity = data.get("severity", None)
    is_phrase = data.get("is_phrase", False)
    context_hint = data.get("context_hint", None)
    created_by_user = True
    is_enabled = data.get("is_enabled", True)
    category_id = None

    db = get_db()

    cursor = db.execute(
        "SELECT id FROM languages WHERE english_name = ? OR native_name = ? OR iso_code = ?",
        (language, language, language),
    )
    language_row = cursor.fetchone()

    if not language_row:
        return {"error": "Language not found"}, 404
    language_id = language_row["id"]

    if category is not None:
        cursor = db.execute(
            "SELECT id FROM categories WHERE category_name = ?",
            (category,),
        )
        category_row = cursor.fetchone()

        if not category_row:
            return {"error": "Category not found"}, 404
        category_id = category_row["id"]

    db.execute(
        "INSERT INTO profanities (profanity_name, language_id, category_id) VALUES (?, ?, ?)",
        (profanity, language_id, category_id),
    )
    db.commit()
    return {"message": "Profanity added successfully"}, 201


@profanities_blueprint.route("/check", methods=["GET"])
def check():
    profanity = request.args.get("profanity", None)

    db = get_db()
    cursor = db.execute(
        "SELECT * FROM profanities WHERE profanity_name = ?", (profanity,)
    )
    result = cursor.fetchone()

    if result:
        return {"exists": True, "profanity": dict(result)}, 200
    else:
        return {"exists": False}, 404
