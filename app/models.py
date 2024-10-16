import sqlalchemy as sa
import sqlalchemy.orm as so

from app import db

liked_meals = sa.Table(
    'liked_meals',
    db.metadata,
    sa.Column('diner_id', sa.Integer, sa.ForeignKey('character.id'), primary_key=True),
    sa.Column('dish_id', sa.Integer, sa.ForeignKey('menu.id'), primary_key=True)
)

liked_teas = sa.Table(
    'liked_teas',
    db.metadata,
    sa.Column('character_id', sa.Integer, sa.ForeignKey('character.id'), primary_key=True),
    sa.Column('tea_id', sa.Integer, sa.ForeignKey('tea.id'), primary_key=True)
)

liked_tea_topics = sa.Table(
    'liked_tea_topics',
    db.metadata,
    sa.Column('character_id', sa.Integer, sa.ForeignKey('character.id'), primary_key=True),
    sa.Column('topic_id', sa.Integer, sa.ForeignKey('tea_topic.id'), primary_key=True)
)

liked_gifts = sa.Table(
    'liked_gifts',
    db.metadata,
    sa.Column('character_id', sa.Integer, sa.ForeignKey('character.id'), primary_key=True),
    sa.Column('gift_id', sa.Integer, sa.ForeignKey('gift.id'), primary_key=True)
)

class Character(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    nickname: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True, nullable=True)

    likes: so.WriteOnlyMapped['Menu'] = so.relationship(secondary=liked_meals, back_populates='liked')
    likes_tea: so.WriteOnlyMapped['Tea'] = so.relationship(secondary=liked_teas, back_populates='liked_tea')
    likes_tea_topic: so.WriteOnlyMapped['TeaTopic'] = so.relationship(secondary=liked_tea_topics,
                                                                      back_populates='liked_tea_topic')
    final_tea_comment: so.Mapped[list['TeaFinalTopic']] = so.relationship("TeaFinalTopic",
                                                                          back_populates="commenter")
    lost_items: so.Mapped[list['TeaFinalTopic']] = so.relationship("LostItem", back_populates="owner")
    likes_gift: so.Mapped['Gift'] = so.relationship(secondary=liked_gifts, back_populates='liked_by')

    def __repr__(self):
        return '<Character {}>'.format(self.name)

class Menu(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    meal: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)

    liked: so.WriteOnlyMapped['Character'] = so.relationship(secondary=liked_meals, back_populates='likes')

    def __repr__(self):
        return '<Menu {}>'.format(self.meal)

class Tea(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)

    liked_tea: so.WriteOnlyMapped['Character'] = so.relationship(secondary=liked_teas, back_populates='likes_tea')

    def __repr__(self):
        return '<Tea {}>'.format(self.name)

class TeaTopic(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    data: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)

    liked_tea_topic: so.WriteOnlyMapped['Character'] = so.relationship(secondary=liked_tea_topics,
                                                                       back_populates='likes_tea_topic')

    def __repr__(self):
        return '<TeaTopic {}>'.format(self.data)

class TeaFinalTopic(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    comment: so.Mapped[str] = so.mapped_column(sa.String(160), index=True, unique=True)
    response: so.Mapped[str] = so.mapped_column(sa.String(64))

    character_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('character.id'))

    commenter: so.Mapped["Character"] = so.relationship("Character", back_populates="final_tea_comment")

    def __repr__(self):
        return '<TeaFinalTopic {}>'.format(self.comment)

class LostItem(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)

    character_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('character.id'))

    owner: so.Mapped["Character"] = so.relationship("Character", back_populates="lost_items")

    def __repr__(self):
        return '<LostItem {}>'.format(self.name)

class Gift(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)

    liked_by: so.Mapped['Character'] = so.relationship(secondary=liked_gifts, back_populates='likes_gift')

    def __repr__(self):
        return '<Gift {}>'.format(self.name)

class Seed(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    grade: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    rank: so.Mapped[int] = so.mapped_column(sa.Integer)

    def __repr__(self):
        return '<Seed {}>'.format(self.name)

class LectureQuestion(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    question: so.Mapped[str] = so.mapped_column(sa.String(256), index=True, unique=True, nullable=False)
    answer: so.Mapped[str] = so.mapped_column(sa.String(128), unique=True, nullable=False)

    def __repr__(self):
        return '<LectureQuestion {}>'.format(self.question)
