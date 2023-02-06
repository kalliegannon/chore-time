from app import db

class User(db.Model):
    user_name = db.Column(db.String)
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer, db.ForeignKey("group.group_id"))
    chore = db.relationship("Chore", back_populates="users")
    group = db.relationship("Group", back_populates="users")