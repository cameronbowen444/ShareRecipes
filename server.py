from flask_app import app
from flask_app.controllers import users, recipes
from flask_app.config.init_db import initialize_database
import os


if __name__ == "__main__":
    initialize_database()

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )