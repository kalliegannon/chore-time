from app import db
# Name
# Unique Identifier
# Users in Group
# Users that are Admin in group
# List of Task in this group

class Group(db.Model):
    name = db.Column(db.String)
    group_id = db.Column(db.integer, primary_key=True, autoincrement=True)
    group_users = db.Column(db.String)