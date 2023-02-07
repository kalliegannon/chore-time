from app import db

class Household(db.Model):

    name = db.Column(db.String)
    household_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    members = db.relationship("Member", back_populates="household")