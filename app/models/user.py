from app import db
# First Name
# Last Name
# Unique Identifier
# List of Households I belong to

class User(db.Model):
    user_name = db.Column(db.String)
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chore_id = db.Column(db.Integer, db.ForeignKey("chore.chore_id"))
    chore = db.relationship("Chore", back_populates="users")
    group = db.relationship("Group", back_populates="users")