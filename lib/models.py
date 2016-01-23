# from flask.ext.sqlalchemy import SQLAlchemy
# db = SQLAlchemy()
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
class_registry={}
Base = declarative_base(class_registry=class_registry)


class Submission(Base):
    __tablename__ = 'Submission'
    id = Column(Integer, primary_key=True)
    team = Column(String(200), nullable=False)
    problem = Column(String(200), nullable=False)
    answer = Column(Text(), nullable=False)
    # submitted = Column(Float(), nullable=False)
    submitted = Column(DateTime(), nullable=False)
    score = Column(Integer, default=0, nullable=False)
    points = Column(Integer, default=0, nullable=False)
    judge_response = Column(Text())

    def __init__(self, team, problem, answer, submitted=None, score=0, points=0, judge_response=None):
        self.team = team
        self.problem = problem
        self.answer = answer
        if submitted is None:
            self.submitted = datetime.datetime.now()
        else:
            self.submitted = submitted
        self.score = score
        self.points = points
        self.judge_response = judge_response


class Balloon(Base):
    __tablename__ = 'Balloon'
    balloon_id = Column(Integer, primary_key=True)
    submission_id = Column(Integer, ForeignKey('Submission.id'), primary_key=True)
    # team = Column(String(200), nullable=False)
    # problem = Column(String(200), nullable=False)
    delivered = Column(Boolean, default=False, nullable=False)

    def __init__(self, submission_id):
        self.submission_id = submission_id


def get_db(conn_string, engine=False):
    db_engine = create_engine(conn_string, convert_unicode=True, client_encoding='utf8')
    db = sessionmaker(bind=db_engine)
    if engine:
        return db, db_engine
    else:
        return db


def set_contest_id(contest_id):
    for table in Base.metadata.tables.values():
        table.name = '%s_%s' % (contest_id, table.name)
    for c in Base._decl_class_registry.values():
        if hasattr(c, '__tablename__'):
            c.__tablename__ = "%s_%s" % (contest_id, c.__tablename__)


def register_base(db):
    db.Model = Base
    for k, c in Base._decl_class_registry.items():
        if k.startswith('_'): continue # SQLAlchemy internal classes
        # Add the query class to each of the models.
        c.query = db.session.query_property()
