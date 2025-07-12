from sqlalchemy import Column, Integer, String, Text, UniqueConstraint, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True)
    stage = Column(String, nullable=False)
    dict_index = Column(Integer, default=0)
    brute_len = Column(Integer, default=1)
    brute_index = Column(Integer, default=0)

    __table_args__ = (Index("ix_progress_stage", "stage"),)


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)
    content = Column(Text)

    __table_args__ = (
        UniqueConstraint("code", name="_results_code_uc"),
        Index("ix_results_code", "code"),
    )


class RetryQueue(Base):
    __tablename__ = "retry_queue"

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)

    __table_args__ = (
        UniqueConstraint("code", name="_retry_code_uc"),
        Index("ix_retry_code", "code"),
    )
