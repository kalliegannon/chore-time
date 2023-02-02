from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.user import User
from app.models.group import Group
from app.models.chore import Chore

def validate_models(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))
    return model

homepage_bp = Blueprint('homepage_bp', __name__)

@homepage_bp.route('/', methods=['GET'])
def read_homepage():
    return 'Welcome to our homepage!'

###########################  Chore Routes  ##############################
chores_bp = Blueprint('chores_bp', __name__, url_prefix='/chores')

# read all chores from one user

@users_bp.route('/<user_id>/chores', methods=['GET'])
def read_chores(user_id):
    user = validate_models(User, user_id)
    chores = Chore.query.all()

    chores_response = []
    for chore in chores:
        if chore.user_id == user.user_id:
            chores_response.append(
        {
            "chore_id": chore.chore_id,
            "title": chore.title,
            "description": chore.description
        }
        )
    return jsonify(chores_response)