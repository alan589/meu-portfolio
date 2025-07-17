from typing import Optional, List
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login



association_table = sa.Table(
    "association_table",
    db.metadata,
    sa.Column("post_id", sa.ForeignKey("post_table.id"), primary_key=True),
    sa.Column("tag_id", sa.ForeignKey("tag_table.id"), primary_key=True),
)

class Post(db.Model):
    __tablename__ = "post_table"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(250), unique=True, index=True)
    subtitle: so.Mapped[str] = so.mapped_column(sa.String(250))
    name: so.Mapped[str] = so.mapped_column(sa.String(100), index=True)
    date: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    body: so.Mapped[str] = so.mapped_column(sa.Text)
    img_url: so.Mapped[str] = so.mapped_column(sa.String(250))
    update_date: so.Mapped[Optional[datetime]]

    tags: so.Mapped[List['Tag']] = so.relationship(
        secondary=association_table, back_populates="posts"
    )

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user_table.id'),
                                               index=True)
    author: so.Mapped['User'] = so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.title)

class Tag(db.Model):
    __tablename__ = "tag_table"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(50), unique=True, index=True)

    posts: so.Mapped[List[Post]] = so.relationship(
        secondary=association_table, back_populates="tags"
    )

    def __repr__(self):
        return '<Tag {}>'.format(self.name)

class User(db.Model, UserMixin):
    __tablename__ = "user_table"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    email: so.Mapped[str] = so.mapped_column(
        sa.String(100), unique=True, index=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(50))
    username: so.Mapped[str] = so.mapped_column(sa.String(50))

    posts: so.Mapped[List[Post]] = so.relationship(
        back_populates='author')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))