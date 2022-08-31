from api import db


class Students(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=100), nullable=False)
    age = db.Column(db.Integer(), nullable=False)

    def __repr__(self) -> str:
        return self.name

