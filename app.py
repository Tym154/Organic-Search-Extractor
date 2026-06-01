import logging

from flask import Flask, render_template

from config import Config
from routes.health import health_bp
from routes.search import search_bp

# Sets a standard logging format including the exact time, the module that fired the log, the severity and the message.
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL, logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_app() -> Flask:
    # Config validation before starting
    Config.validate()

    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(search_bp)
    app.register_blueprint(health_bp)

    @app.route("/")
    def index() -> str:
        return render_template("index.html")

    logger.info(f"Application started in {Config.FLASK_ENV} mode.")
    return app


app = create_app()


# DEV: This block only executes if you run `python app.py` directly.
# In production (Docker), Gunicorn imports the `app` object and bypasses this block.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT)
