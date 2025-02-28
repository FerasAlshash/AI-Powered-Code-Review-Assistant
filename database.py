from peewee import *
from datetime import datetime

db = SqliteDatabase('code_reviews.db')

class BaseModel(Model):
    class Meta:
        database = db

class CodeReview(BaseModel):
    code = TextField()
    review = TextField()
    created_at = DateTimeField(default=datetime.now)

class Conversation(BaseModel):
    code_review = ForeignKeyField(CodeReview, backref='conversations')
    question = TextField()
    answer = TextField()
    created_at = DateTimeField(default=datetime.now)

def initialize_db():
    db.connect()
    db.create_tables([CodeReview, Conversation])
    db.close()

def save_review(code, review):
    review = CodeReview.create(
        code=code,
        review=review
    )
    return review

def save_conversation(code_review_id, question, answer):
    conversation = Conversation.create(
        code_review=code_review_id,
        question=question,
        answer=answer
    )
    return conversation

def get_recent_reviews(limit=5):
    return (CodeReview
            .select()
            .order_by(CodeReview.created_at.desc())
            .limit(limit))

def get_conversations(code_review_id):
    return (Conversation
            .select()
            .where(Conversation.code_review == code_review_id)
            .order_by(Conversation.created_at))

def delete_review(review_id):
    Conversation.delete().where(Conversation.code_review == review_id).execute()
    CodeReview.delete().where(CodeReview.id == review_id).execute()

if __name__ == '__main__':
    initialize_db()
