from flask import Flask, g
from api.routes import register_routes

app = Flask(__name__)


# Close the DB when the request ends
@app.teardown_appcontext
def close_db(_):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    return "Hello, World!"


# Register routes
register_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
