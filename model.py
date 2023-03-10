import sqlalchemy as sql
from database import Base,engine

class Count(Base):
    __tablename__ = "count"

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    uuid = sql.Column(sql.String, unique = True)
    count = sql.Column(sql.Integer)

    def __init__(self,uuid,count):
        self.uuid = uuid
        self.count = count

    def __repr__(self) -> str:
        return f"{self.uuid}"


Base.metadata.create_all(bind=engine)