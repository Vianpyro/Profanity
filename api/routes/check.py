from flask import Blueprint, request

from api.database import get_db
from api.utility import make_uniform_string, translate_special_chars

check_blueprint = Blueprint("check", __name__)


@check_blueprint.route("/", methods=["POST"])
def check():
    data = request.get_json()
    word = make_uniform_string(data.get("word"))
    word_alt = translate_special_chars(word)

    db = get_db()
    cursor = db.execute(
        "SELECT * FROM profanities WHERE profanity_name = ?",
        (word,),
    )
    result = cursor.fetchone()

    if result:
        return dict(result), 200

    return {"error": "Profanity not found"}, 404


@check_blueprint.route("/sentence", methods=["POST"])
def check_sentence():
    data = request.get_json()
    words = [make_uniform_string(word) for word in data["sentence"].split()]
    placeholders = ",".join("?" for _ in words)

    db = get_db()
    cursor = db.execute(
        f"SELECT * FROM profanities WHERE profanity_name IN ({placeholders})",
        tuple(words),
    )
    results = cursor.fetchall()

    if results:
        return [dict(row) for row in results], 200

    return {"error": "No profanities found"}, 404
