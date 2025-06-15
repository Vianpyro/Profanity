from flask import Blueprint, request

from api.database import get_db

languages_blueprint = Blueprint("languages", __name__)


@languages_blueprint.route("/", methods=["GET"])
def list_items():
    language_id = request.args.get("id")
    iso_code = request.args.get("locale")
    language = request.args.get("name")

    db = get_db()

    if language_id:
        cursor = db.execute("SELECT * FROM languages WHERE id = ?", (language_id,))
        language = cursor.fetchone()
        if language:
            return {"language": dict(language)}, 200
        return {"error": "Language not found"}, 404

    if iso_code:
        cursor = db.execute("SELECT * FROM languages WHERE iso_code = ?", (iso_code,))
        language = cursor.fetchone()
        if language:
            return {"language": dict(language)}, 200
        return {"error": "Language not found"}, 404

    if language:
        cursor = db.execute(
            "SELECT * FROM languages WHERE english_name = ? OR native_name = ? OR iso_code = ?",
            (language, language, language),
        )
        language = cursor.fetchone()
        if language:
            return {"language": dict(language)}, 200
        return {"error": "Language not found"}, 404

    # If no filters are provided, return all languages

    cursor = db.execute("SELECT * FROM languages")
    return [dict(lang) for lang in cursor.fetchall()], 200


@languages_blueprint.route("/add", methods=["POST"])
def add():
    data = request.get_json()
    english_name = data.get("english_name")
    native_name = data.get("native_name", None)
    iso_code = data.get("locale")

    db = get_db()
    db.execute(
        "INSERT INTO languages (english_name, native_name, iso_code) VALUES (?, ?, ?)",
        (english_name, native_name, iso_code),
    )
    db.commit()
    return {"message": "Language added successfully"}, 201
