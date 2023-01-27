from app import db
# Title /////
# Description/////
# Unique Identifier////
# Date Due
# Assigned User
# Group Owner

class Chore(db.Model):
    chore_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    