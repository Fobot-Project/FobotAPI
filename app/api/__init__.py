from flask import Blueprint

bp = Blueprint('api', __name__)


@bp.route('/ping', methods=['GET'])
def ping():
    return "ping!"