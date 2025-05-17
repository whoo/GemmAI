from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey,DateTime , UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base, mapped_column, Mapped
from sqlalchemy.types import Uuid

from flask_login import UserMixin

from werkzeug.security import check_password_hash,generate_password_hash
import uuid

from sqlalchemy.dialects.postgresql import UUID


Base=declarative_base()


class User(Base, UserMixin ):
      __tablename__  = 'users'
      __table_args__ = ( UniqueConstraint("id"),)
      id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
      username : Mapped[str] = mapped_column("username",String(30))
      password : Mapped[str] = mapped_column( nullable=True)

      def __repr__(self) -> str:
          return f"User({self.username}-{self.id})"

      def save(self):
          self.query.session.add(self)
          return self.query.session.commit()
      
      def delete(self):
          self.query.session.delete(self)
          r=self.query.session.commit()
          self.id=None
          self.username=None
          self.password=None
          return r


      def setpassword(self,password):
          cr = generate_password_hash(password)
          self.password=cr
          return 1

      def get_id(self):
          #print("Get ID")
          #print(self.id)          
          return self.id

      def __init__(self,username,password):
          self.username=username
          self.setpassword(password)


class Role(Base):
      __tablename__ = "roles"
      id: Mapped[uuid.UUID] = mapped_column(primary_key=True,default=uuid.uuid4)
      role: Mapped[str] = mapped_column("role",String(30))


def create_tables(engine):
    Base.metadata.create_all(engine)


