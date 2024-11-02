"""Define database models used in the application.

This module contains SQLAlchemy models that represent the database schema.

Classes:
    - Character: Represents a character in FE16.
    - Menu: Represents a dining hall meal.
    - Tea: Represents a tea option.
    - TeaTopic: Represents a tea party topic.
    - TeaFinalTopic: Represents a tea party final comment and response.
    - LostItem: Represents a lost monastery item.
    - Gift: Represents a gift item.
    - Seed: Represents a plantable seed.
    - LectureQuestion: Represents a monthly lecture question and answer.

Relationships:
    - liked_meals: Links characters and liked meals.
    - liked_teas: Links characters and liked teas.
    - liked_tea_topics: Links characters and interested tea party topics.
    - liked_gifts: Links characters and liked gifts.
"""


import sqlalchemy as sa
import sqlalchemy.orm as so

from app import db


liked_meals = sa.Table(
    'liked_meals',
    db.metadata,
    sa.Column('diner_id', sa.Integer, sa.ForeignKey('character.id'), primary_key=True),
    sa.Column('dish_id', sa.Integer, sa.ForeignKey('menu.id'), primary_key=True)
)
"""Association table to link characters with meals they like.

Columns:
    diner_id (int): Foreign key referencing the character's ID.
    dish_id (int): Foreign key referencing the meal's ID.
"""

liked_teas = sa.Table(
    'liked_teas',
    db.metadata,
    sa.Column('character_id', sa.Integer, sa.ForeignKey('character.id'), primary_key=True),
    sa.Column('tea_id', sa.Integer, sa.ForeignKey('tea.id'), primary_key=True)
)
"""Association table to link characters with teas they like.

Columns:
    character_id (int): Foreign key referencing the character's ID.
    tea_id (int): Foreign key referencing the tea's ID.
"""

liked_tea_topics = sa.Table(
    'liked_tea_topics',
    db.metadata,
    sa.Column('character_id', sa.Integer, sa.ForeignKey('character.id'), primary_key=True),
    sa.Column('topic_id', sa.Integer, sa.ForeignKey('tea_topic.id'), primary_key=True)
)
"""Association table to link characters with teas party topics they are interested in.

Columns:
    character_id (int): Foreign key referencing the character's ID.
    topic_id (int): Foreign key referencing the topic's ID.
"""

liked_gifts = sa.Table(
    'liked_gifts',
    db.metadata,
    sa.Column('character_id', sa.Integer, sa.ForeignKey('character.id'), primary_key=True),
    sa.Column('gift_id', sa.Integer, sa.ForeignKey('gift.id'), primary_key=True)
)
"""Association table to link characters with gifts they like.

Columns:
    character_id (int): Foreign key referencing the character's ID.
    gift_id (int): Foreign key referencing the gift's ID.
"""


class Character(db.Model):
    """Represents a character in FE16.

    Attributes:
        id (int): The unique identifier for the character.
        name (str): The name of the character.
        nickname (str): Alternate name(s) the character is referred by.
        likes (Menu): ORM relationship that defines meals the character likes.
        likes_tea (Tea): ORM relationship that defines tea(s) the character likes.
        likes_tea_topic (TeaTopic): ORM relationship that defines tea party topics the character is interested in.
        final_tea_comment (TeaFinalTopic): ORM relationship that defines tea party final comments the character makes.
        lost_items (LostItem): ORM relationship that defines items the character can lose around the monastery.
        likes_gift (Gift): ORM relationship that defines gifts the character likes.
    """

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    nickname: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True, nullable=True)

    likes: so.WriteOnlyMapped['Menu'] = so.relationship(secondary=liked_meals, back_populates='liked')
    likes_tea: so.WriteOnlyMapped['Tea'] = so.relationship(secondary=liked_teas, back_populates='liked_tea')
    likes_tea_topic: so.WriteOnlyMapped['TeaTopic'] = so.relationship(secondary=liked_tea_topics,
                                                                      back_populates='liked_tea_topic')
    final_tea_comment: so.Mapped[list['TeaFinalTopic']] = so.relationship("TeaFinalTopic",
                                                                          back_populates="commenter")
    lost_items: so.Mapped[list['LostItem']] = so.relationship("LostItem", back_populates="owner")
    likes_gift: so.Mapped['Gift'] = so.relationship(secondary=liked_gifts, back_populates='liked_by')

    def __repr__(self):
        """Return a string representation of the Character object."""
        return '<Character {}>'.format(self.name)


class Menu(db.Model):
    """Represents an available meal at the monastery dining hall.

    Attributes:
        id (int): The unique identifier for the meal.
        meal (str): The name of the meal.
        liked (Character): ORM relationship that defines the characters that like the meal.
    """

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    meal: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)

    liked: so.WriteOnlyMapped['Character'] = so.relationship(secondary=liked_meals, back_populates='likes')

    def __repr__(self):
        """Return a string representation of the Menu object."""
        return '<Menu {}>'.format(self.meal)


class Tea(db.Model):
    """Represents a tea option for tea parties.

    Attributes:
        id (int): The unique identifier for the tea.
        name (str): The name of the tea.
        liked_tea (Character): ORM relationship that defines the characters that like the tea.
    """

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)

    liked_tea: so.WriteOnlyMapped['Character'] = so.relationship(secondary=liked_teas, back_populates='likes_tea')

    def __repr__(self):
        """Return a string representation of the Tea object."""
        return '<Tea {}>'.format(self.name)


class TeaTopic(db.Model):
    """Represents a tea party topic option.

    Attributes:
        id (int): The unique identifier for the topic.
        data (str): The available topic option.
        liked_tea_topic (Character): ORM relationship that defines the characters that like the topic.
    """

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    data: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)

    liked_tea_topic: so.WriteOnlyMapped['Character'] = so.relationship(secondary=liked_tea_topics,
                                                                       back_populates='likes_tea_topic')

    def __repr__(self):
        """Return a string representation of the TeaTopic object."""
        return '<TeaTopic {}>'.format(self.data)


class TeaFinalTopic(db.Model):
    """Represents a tea party final topic comment and responses.

    Attributes:
        id (int): The unique identifier for the final topic.
        comment (str): The final topic comment a character makes.
        response (str): Responses to the comment that garner approval.
        character_id (int): The foreign key that maps to the character that makes the comment.
        commenter (Character): ORM relationship that defines the character that the final topic relates to.
    """

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    comment: so.Mapped[str] = so.mapped_column(sa.String(160), index=True, unique=True)
    response: so.Mapped[str] = so.mapped_column(sa.String(64))

    character_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('character.id'))

    commenter: so.Mapped["Character"] = so.relationship("Character", back_populates="final_tea_comment")

    def __repr__(self):
        """Return a string representation of the TeaFinalTopic object."""
        return '<TeaFinalTopic {}>'.format(self.comment)


class LostItem(db.Model):
    """Represents a lost monastery item.

    Attributes:
        id (int): The unique identifier for the lost item.
        name (str): The name of the lost item.
        character_id (int): The foreign key that maps to the character that lost the item.
        owner (Character): ORM relationship that defines the character that the lost item belongs to.
    """

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)

    character_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('character.id'))

    owner: so.Mapped["Character"] = so.relationship("Character", back_populates="lost_items")

    def __repr__(self):
        """Return a string representation of the LostItem object."""
        return '<LostItem {}>'.format(self.name)


class Gift(db.Model):
    """Represents a gift that can be given to characters.

    Attributes:
        id (int): The unique identifier for the gift.
        name (str): The name of the gift.
        liked_by (Character): ORM relationship that defines the characters that like the gift.
    """

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)

    liked_by: so.Mapped['Character'] = so.relationship(secondary=liked_gifts, back_populates='likes_gift')

    def __repr__(self):
        """Return a string representation of the Gift object."""
        return '<Gift {}>'.format(self.name)


class Seed(db.Model):
    """Represents a seed to plant at the greenhouse.

    Attributes:
        id (int): The unique identifier for the seed.
        name (str): The name of the seed.
        grade (int): The star grade of the seed.
        rank (int): The hidden rank of the seed.
    """

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    grade: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    rank: so.Mapped[int] = so.mapped_column(sa.Integer)

    def __repr__(self):
        """Return a string representation of the Seed object."""
        return '<Seed {}>'.format(self.name)


class LectureQuestion(db.Model):
    """Represents a monthly lecture question and answer pair.

    Attributes:
        id (int): The unique identifier for the question.
        question (str): The question posed to the user.
        answer (str): The answer that grants the most professor points.
    """

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    question: so.Mapped[str] = so.mapped_column(sa.String(256), index=True, unique=True, nullable=False)
    answer: so.Mapped[str] = so.mapped_column(sa.String(128), unique=True, nullable=False)

    def __repr__(self):
        """Return a string representation of the LectureQuestion object."""
        return '<LectureQuestion {}>'.format(self.question)
