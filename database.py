from typing import Union

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.session import Session, sessionmaker


db = SQLAlchemy()
migrate = Migrate(db=db)


def getSession() -> Union[Session, sessionmaker]: return db.session()
