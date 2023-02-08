from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.member import Member
from app.models.household import Household
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


# def validate_models(model_id):
#     try:
#         model_id = int(model_id)
#     except:
#         abort(make_response({"message":f"{model_id} invalid"}, 400))
# #cls to model name
#     model = cls.query.get(model_id)

#     if not model:
#         abort(make_response({"message":f"{model_id} not found"}, 404))
#     return model

# homepage_bp = Blueprint('homepage_bp', __name__)

# @homepage_bp.route('/', methods=['GET'])
# def read_homepage():
#     return 'Welcome to our homepage!'

# ###########################  Chore Routes  ##############################
chores_bp = Blueprint('chores', __name__, url_prefix='/chores')
members_bp = Blueprint('members_bp', __name__, url_prefix='/members')
household_bp = Blueprint('household_bp', __name__, url_prefix='/household')


# # read all chores from one user

@chores_bp.route('', methods=['GET'])
def read_chores():
    # user = validate_models(User, user_id)
    chores = Chore.query.all()

    chores_response = []
    for chore in chores:
        # if chore.user_id == user.user_id:
            chores_response.append(
        {
            # "chore_id": chore.chore_id,
            "title": chore.title,
            "description": chore.description
        }
        )
    print(chores_response)
    return jsonify(chores_response)

#update chore 
# @chores_bp.route('/<chore_id>', methods=["PUT"])
# def update_chore(chore_id):
#     # chore = validate_models(Chore, chore_id)

#     request_body = request.get_json()

#     chore.title = request_body["title"]
#     chore.description = request_body["description"]

#     db.session.commit()

#     return make_response(jsonify("Chore has been updated"))


# create chore inside user
@chores_bp.route('', methods=['POST'])
def create_chore():
    # user = validate_models(User, user_id)
    request_body = request.get_json()
    new_chore = Chore(
        chore_id = request_body["chore_id"],
        title=request_body["title"],
        description=request_body["description"]
    )
    # user.chores.append(new_chore)
    db.session.add(new_chore)
    db.session.commit()

    return make_response(jsonify(f"New Chore {new_chore.title} successfully created"), 201)


# # DELETE chore
# @chores_bp.route('/<chore_id>', methods=['DELETE'])
# def delete_chore(chore_id):
#     chore = validate_models(Chore, chore_id)
#     resopnse = jsonify(f"Chore {chore.chore_id} successfully deleted")
#     db.session.delete(chore)
#     db.session.commit()

#     return make_response(resopnse)
# #check make response in jasonify if issues

# ########################### User Routes ##########################
# # users_bp = Blueprint('users_bp', __name__, url_prefix='/users')
# # read all users from one group
# # groups_bp = Blueprint('groups_bp', __name__, url_prefix='/groups')

# #get one user from group
# @groups_bp.route('/<group_id>/user_id', methods=['GET'])
# def read_one_user_from_group(group_id):
#     group = validate_models(Group, group_id)
    

#     return{
#         "user_id": user.user_id,
#         "user_name": user.name
#     }

# create member inside a household

@members_bp.route('/<household_id>/members', methods=['POST'])
def create_member(household_id):
    household = validate_models(Household, household_id)
    request_body = request.get_json()
    new_member = Member(
        member_name=request_body["member_name"]
    )

    household.members.append(new_member)
    db.session.add(new_member)
    db.session.commit()

    return make_response(jsonify(f"Member message {new_member.member_name} successfully created"), 201)

# DELETE member
@members_bp.route('/<member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = validate_models(Member, member_id)
    response = jsonify(f"member {member.member_id} successfully deleted")
    db.session.delete(member)
    db.session.commit()

    return make_response(response)

# read all member from one group

@members_bp.route('/<household_id>/members', methods=['GET'])
def read_household_members(household_id):
    household = validate_models(Household, household_id)
    members = Member.query.all()

    members_response = []
    for member in members:
        if member.household_id == household.household_id:
            members_response.append(
            {
            "member_id": member.member_id,
            "member_name": member.member_name
            }
        )
    return jsonify(members_response)

# #update user
# @users_bp.route('/<user_id>', methods=["PUT"])
# def update_user(user_id):
#     user = validate_models(User, user_id)

#     request_body = request.get_json()

#     user.name = request_body["name"]

#     db.session.commit()

#     return make_response(jsonify("User has been updated"))



# ############################## GROUP ROUTES ##############################
households_bp = Blueprint('household_bp', __name__, url_prefix='/household')

# get all household
@households_bp.route('', methods=['GET'])
def read_households():
    households = Household.query.all()

    households_response = []
    for household in households:
        households_response.append(
        {
            "household_id": household.household_id,
            "name": household.name
        }
        )
    return jsonify(households_response)

#get one household by household id
@households_bp.route('/<household_id>', methods=['GET'])
def read_one_household(household_id):
    household = validate_models(Household, household_id)

    return{
        "household_id": household.household_id,
        "name": household.name
    }

#update household name
@households_bp.route('/<household_id>', methods=["PUT"])
def update_household(household_id):
    household = validate_models(Household, household_id)

    request_body = request.get_json()

    household.name = request_body["name"]

    db.session.commit()

    return make_response(jsonify("household has been updated"))

#create household
@households_bp.route('', methods=['POST'])
def create_household():
    request_body = request.get_json()
    new_household = Household(
        name=request_body["name"]
    )
    db.session.add(new_household)
    db.session.commit()

    return make_response(jsonify(f"household {new_household.name} successfully created"), 201)

# delete household
@households_bp.route('/<household_id>', methods=['DELETE'])
def delete_household(household_id):
    household = validate_models(Household, household_id)
    response = jsonify(f"household {household.name} successfully deleted")
    db.session.delete(household)
    db.session.commit()

    return make_response(response)