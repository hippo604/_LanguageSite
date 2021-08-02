from langsite import db
import enum


association_table = db.Table('association', db.Model.metadata,
    db.Column('question_id', db.ForeignKey('questions.id'), primary_key=True),
    db.Column('quiz_id', db.ForeignKey('quizzes.id'), primary_key=True)
)

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer,primary_key=True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    quizzes = db.relationship("Quiz",
                    secondary=association_table,
                    backref="questions")

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def __repr__(self):
        return f"Answer to '{self.question}' is '{self.answer}'."

#https://medium.com/the-andela-way/how-to-create-django-like-choices-field-in-flask-sqlalchemy-1ca0e3a3af9d
class QuizStatusEnum(enum.Enum):
    not_ready = 'NOT_READY'
    ready_to_test = 'READY_TO_TEST'

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.Integer,default=1)
    status = db.Column(db.Enum(QuizStatusEnum), default=QuizStatusEnum.not_ready, nullable=False)
