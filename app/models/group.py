from app import db

class Group(db.Model):
    name = db.Column(db.String)
    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    user = db.relationship("User", back_populates="groups")