from app import db

class Member(db.Model):
    member_name = db.Column(db.String)
    member_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    household_id = db.Column(db.Integer, db.ForeignKey("household.household_id"))
    chores = db.relationship("Chore", back_populates="member")
    household = db.relationship("Household", back_populates="members")