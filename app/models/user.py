from app import db
# First Name
# Last Name
# Unique Identifier
# List of Households I belong to

class User(db.Model):
    user_name = db.Column(db.String)
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chore = db.relationship("Chore", back_populates="User")