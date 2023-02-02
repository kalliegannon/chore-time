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


# create chore inside user
@users_bp.route('/<user_id>/chores', methods=['POST'])
def create_chore(user_id):
    user = validate_models(User, user_id)
    request_body = request.get_json()
    new_chore = Chore(
        title=request_body["title"],
        description=request_body["description"]
    )

    user.chores.append(new_chore)
    db.session.add(new_chore)
    db.session.commit()

    return make_response(jsonify(f"New Chore {new_chore.title} successfully created"), 201)


# DELETE chore
@chores_bp.route('/<chore_id>', methods=['DELETE'])
def delete_chore(chore_id):
    chore = validate_models(Chore, chore_id)

    db.session.delete(chore)
    db.session.commit()

    return make_response(jsonify(f"Chore {chore.chore_id} successfully deleted"))


########################### User Routes ##########################
user_bp = Blueprint('users_bp', __name__, url_prefix='/users')
# read all users from one group
@groups_bp.route('/<group_id>/users', methods=['GET'])
def read_users(group_id):
    group = validate_models(Group, group_id)
    users = User.query.all()

    users_response = []
    for user in users:
        if user.group_id == group.group_id:
            users_response.append(
            {
            "user_id": user.user_id,
            "title": user.name
            }
        )
    return jsonify(users_response)
