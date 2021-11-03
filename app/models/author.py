from app import db

class Author(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(200))
  books = db.relationship("Book", back_populates="author")