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
            "name": user.name
            }
        )
    return jsonify(users_response)

# create user inside a group
@groups_bp.route('/<group_id>/users', methods=['POST'])
def create_user(group_id):
    group = validate_models(Group, group_id)
    request_body = request.get_json()
    new_user = User(
        user_name=request_body["name"]
    )

    group.users.append(new_user)
    db.session.add(new_user)
    db.session.commit()

    return make_response(jsonify(f"User message {new_user.user_name} successfully created"), 201)

# DELETE user
@users_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = validate_models(User, user_id)

    db.session.delete(user)
    db.session.commit()

    return make_response(jsonify(f"User {user.user_id} successfully deleted"))

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
            "name": user.name
            }
        )
    return jsonify(users_response)


############################## GROUP ROUTES ##############################
group_bp = Blueprint('groups_bp', __name__, url_prefix='/groups')

# get all groups
@groups_bp.route('', methods=['GET'])
def read_groups():
    groups = Group.query.all()

    groups_response = []
    for group in groups:
        groups_response.append(
        {
            "group_id": group.group_id,
            "name": name.title
        }
        )
    return jsonify(groups_response)

#get one group by group id
@groups_bp.route('/<group_id>', methods=['GET'])
def read_one_group(group_id):
    group = validate_models(Group, group_id)

    return{
        "group_id": group.group_id,
        "name": group.name
    }

#update group name
@groups_bp.route('/<group_id>', methods=["PUT"])
def update_group(group_id):
    group = validate_models(Group, group_id)

    request_body = request.get_json()

    group.name = request_body["name"]

    db.session.commit()

    return make_response(jsonify("Group has been updated"))