from .categories import categories_blueprint
from .contextual_rules import contextual_rules_blueprint
from .languages import languages_blueprint
from .profanities import profanities_blueprint
from .replacements import replacements_blueprint


def register_routes(app):
    app.register_blueprint(categories_blueprint, url_prefix="/category")
    app.register_blueprint(contextual_rules_blueprint, url_prefix="/rule")
    app.register_blueprint(languages_blueprint, url_prefix="/language")
    app.register_blueprint(replacements_blueprint, url_prefix="/replacement")
    app.register_blueprint(profanities_blueprint, url_prefix="/profanity")
