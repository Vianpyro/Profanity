from flask import Blueprint, request

from api.database import get_db

replacements_blueprint = Blueprint("replacements", __name__)


@replacements_blueprint.route("/", methods=["GET"])
def list_items():
    db = get_db()
    cursor = db.execute("SELECT * FROM replacements")
    return [dict(replacement) for replacement in cursor.fetchall()], 200


@replacements_blueprint.route("/add", methods=["POST"])
def add():
    data = request.get_json()
    language = data.get("language")
    profanity = data.get("profanity")
    replacement_text = data.get("replacement_text", None)

    db = get_db()

    cursor = db.execute(
        "SELECT id FROM languages WHERE english_name = ? OR native_name = ? OR iso_code = ?",
        (language, language, language),
    )
    language_row = cursor.fetchone()

    if not language_row:
        return {"error": "Language not found"}, 404
    language_id = language_row["id"]

    cursor = db.execute(
        "SELECT id FROM profanities WHERE profanity_name = ? AND language_id = ?",
        (profanity, language_id),
    )
    profanity_row = cursor.fetchone()

    if not profanity_row:
        return {"error": "Profanity not found"}, 404
    profanity_id = profanity_row["id"]

    db.execute(
        "INSERT INTO replacements (replacement_text, profanity_id, language_id) VALUES (?, ?, ?)",
        (replacement_text, profanity_id, language_id),
    )
    db.commit()
    return {"message": "Replacement added successfully"}, 201
