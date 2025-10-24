from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class HashtagFeedback(Base):
    __tablename__ = "hashtag_feedback"
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    hashtags = Column(Text)
    user_feedback = Column(Integer)


engine = create_engine("sqlite:///database/local_database.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_feedback(text, hashtags, user_feedback):
    feedback = HashtagFeedback(
        text=text,
        hashtags=hashtags,
        user_feedback=user_feedback
    )
    session.add(feedback)
    session.commit()


