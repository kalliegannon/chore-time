from app import db


class Chore(db.Model):
    chore_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    member_id = db.Column(db.Integer, db.ForeignKey("member.member_id"))
    member = db.relationship("Member", back_populates="chores")

