from flask import Blueprint, jsonify
from flask.typing import ResponseReturnValue

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check() -> ResponseReturnValue:
    return jsonify({"status": "ok"}), 200
