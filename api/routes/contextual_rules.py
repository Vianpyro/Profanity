from flask import Blueprint, request

from api.database import get_db

contextual_rules_blueprint = Blueprint("contextual_rules", __name__)


@contextual_rules_blueprint.route("/", methods=["GET"])
def list_items():
    db = get_db()
    cursor = db.execute("SELECT * FROM contextual_rules")
    return [dict(rule) for rule in cursor.fetchall()], 200


@contextual_rules_blueprint.route("/add", methods=["POST"])
def add():
    data = request.get_json()
    rule_name = data.get("name")
    profanity = data.get("profanity")
    language = data.get("language")
    rule_type = data.get("type")
    pattern = data.get("pattern", None)
    is_safe = data.get("is_safe", False)

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
        """INSERT INTO contextual_rules (
            profanity_id,
            rule_name,
            rule_type,
            pattern,
            is_safe
        ) VALUES (?, ?, ?, ?, ?)
        """,
        (profanity_id, rule_name, rule_type, pattern, is_safe),
    )
    db.commit()
    return {"message": "Contextual rule added successfully"}, 201
