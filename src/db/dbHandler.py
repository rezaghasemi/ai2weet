from omegaconf import OmegaConf

from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
cfg = OmegaConf.load("src/configs/configs.yaml")


class genContent(Base):
    __tablename__ = "generated_content"
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    hashtags = Column(Text)
    user_feedback = Column(Integer)


engine = create_engine(cfg.database.path)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_feedback(id, user_feedback = 0):
    # Fetch the record
    feedback = session.query(genContent).filter(genContent.id == id).first()
    # if record exists
    if feedback:
        # Update the field
        feedback.user_feedback = user_feedback
        # Commit the change
        session.commit()
        return feedback
    return None


def add_generated_content(description, hashtags, image_url):
    feedback = genContent(
        text=description,
        hashtags=",".join(hashtags),
        user_feedback=0
    )
    session.add(feedback)
    session.commit()
    return feedback.id  


def get_all_feedback():
    return session.query(genContent).all()