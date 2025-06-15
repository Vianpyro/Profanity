from enum import Enum

from flask import Blueprint, request

from api.database import get_db
from api.utility import make_uniform_string, translate_special_chars

profanities_blueprint = Blueprint("profanities", __name__)


class ProfanityLevel:
    UNKNOWN = "unknown"
    LOW = "mild"
    MEDIUM = "moderate"
    HIGH = "severe"

    @classmethod
    def choices(cls):
        return [cls.UNKNOWN, cls.LOW, cls.MEDIUM, cls.HIGH]


class ProfanityCategory(Enum):
    UNKNOWN = "Unknown"
    DISCRIMINATION = "Discrimination"
    INSULTS = "Insults"
    POLITICAL = "Political"
    RELIGIOUS = "Religious"
    RACIAL = "Racial"
    SEXUAL = "Sexual"
    SLANG = "Slang"
    VIOLENT = "Violent"


@profanities_blueprint.route("/", methods=["GET"])
def list_items():
    db = get_db()
    cursor = db.execute("SELECT * FROM profanities")
    return [dict(profanity) for profanity in cursor.fetchall()], 200


@profanities_blueprint.route("/add", methods=["POST"])
def add():
    data = request.get_json()

    profanity = make_uniform_string(data.get("profanity"))
    alt_profanity = translate_special_chars(profanity)
    language = data.get("language")
    category = data.get("category")
    severity = ProfanityLevel.choices()[data.get("severity", 0)]
    severity = (
        severity if severity in ProfanityLevel.choices() else ProfanityLevel.UNKNOWN
    )
    context_hint = data.get("context_hint")
    replacement = data.get("replacement")
    replacement_note = data.get("replacement_hint")
    is_phrase = " " in data.get("profanity")
    created_by_user = True
    is_enabled = True

    db = get_db()

    def get_id(query, value, label):
        cursor = db.execute(
            query, (value, value, value) if label == "language" else (value,)
        )
        row = cursor.fetchone()
        if not row:
            return None
        return row["id"]

    language_id = get_id(
        "SELECT id FROM languages WHERE english_name = ? OR native_name = ? OR iso_code = ?",
        language,
        "language",
    )
    if not language_id:
        return {"error": "Language not found"}, 404

    category_id = None
    if category:
        category_id = get_id(
            "SELECT id FROM categories WHERE category_name = ?",
            category,
            "category",
        )
        if not category_id:
            return {"error": "Category not found"}, 404

    def insert_profanity(name):
        db.execute(
            """
            INSERT INTO profanities (
                profanity_name, language_id, category_id, severity_level,
                is_phrase, context_hint, created_by_user, is_enabled
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                language_id,
                category_id,
                severity,
                is_phrase,
                context_hint,
                created_by_user,
                is_enabled,
            ),
        )

    insert_profanity(profanity)
    if profanity != alt_profanity:
        insert_profanity(alt_profanity)
    db.commit()

    if replacement:
        cursor = db.execute(
            "SELECT id FROM profanities WHERE profanity_name = ?", (profanity,)
        )
        profanity_row = cursor.fetchone()
        if not profanity_row:
            return {"error": "Profanity not found after insertion"}, 404

        db.execute(
            "INSERT INTO replacements (profanity_id, replacement_text, note) VALUES (?, ?, ?)",
            (profanity_row["id"], replacement, replacement_note),
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
