from enum import unique
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

liked_meals = sa.Table(
    'liked_meals',
    db.metadata,
    sa.Column('diner_id', sa.Integer, sa.ForeignKey('character.id'), primary_key=True),
    sa.Column('dish_id', sa.Integer, sa.ForeignKey('menu.id'), primary_key=True)
)

class Character(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    nickname: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True, nullable=True)

    likes: so.WriteOnlyMapped['Menu'] = so.relationship(secondary=liked_meals, back_populates='liked')

    def __repr__(self):
        return '<Character {}>'.format(self.name)

class Menu(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    meal: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)

    liked: so.WriteOnlyMapped['Character'] = so.relationship(secondary=liked_meals, back_populates='likes')

    def __repr__(self):
        return '<Menu {}>'.format(self.meal)