from langsite import db
import enum


class Association(db.Model):
    __tablename__ = 'association'
    quiz_id = db.Column(db.ForeignKey('quizzes.id'),primary_key=True)
    question_id = db.Column(db.ForeignKey('questions.id'),primary_key=True)
    question = db.relationship("Question", back_populates="quizzes")
    quiz = db.relationship("Quiz", back_populates="questions")
    comment = db.Column(db.String(50))
    result = db.Column(db.String(50))
    result_comment = db.Column(db.String(50))

#https://medium.com/the-andela-way/how-to-create-django-like-choices-field-in-flask-sqlalchemy-1ca0e3a3af9d
class QuizStatusEnum(enum.Enum):
    not_ready = 'NOT_READY'
    ready_to_test = 'READY_TO_TEST'

class Quiz(db.Model):
    __tablename__ = "quizzes"
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.Integer,default=1)
    status = db.Column(db.Enum(QuizStatusEnum), default=QuizStatusEnum.not_ready, nullable=False)
    questions = db.relationship("Association", back_populates="quiz")

class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer,primary_key=True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    comment = db.Column(db.Text)
    quizzes =db.relationship("Association", back_populates="question")

    def __init__(self, question, answer, comment=None):
        self.question = question
        self.answer = answer
        self.comment = comment

    def __repr__(self):
        return f"Answer to '{self.question}' is '{self.answer}'."
