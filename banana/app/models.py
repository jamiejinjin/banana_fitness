from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import db,appbuilder
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime
from flask import g

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""


class questionModel(Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), )
    content = db.Column(db.Text)
    created_at = db.Column(
        db.DateTime, default=datetime.now, nullable=True)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=True)

    @declared_attr
    def user_id(self):
        return db.Column(db.Integer, db.ForeignKey("ab_user.id"),
                         default=self.get_user_id, nullable=True)

    @classmethod
    def get_user_id(cls):
        try:
            return g.user.id
        except Exception as e:
            return None
    user =  db.relationship(appbuilder.sm.user_model)

    def __repr__(self):
        return "%s--by[%s]"%(self.title,self.user)

class answerModel(Model):
    __tablename__ = "answers"
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey(questionModel.id))
    question = db.relationship(questionModel, backref = "answers")
    content = db.Column(db.Text)
    created_at = db.Column(
        db.DateTime, default=datetime.now, nullable=True)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=True)
