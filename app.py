from langsite import app,db
from langsite.models.models import Question,QuizStatusEnum,Quiz,Association
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,FormField,FieldList,Form,HiddenField
from collections import namedtuple

################################################################
################################################################
class QuestionEditForm(FlaskForm):
    FormQuestion = StringField("Question")
    FormSubmit =SubmitField('Submit')

###

class QuestionForm(Form):
    question_id = StringField('ID')
    question = StringField('質問')
    answer = StringField('答え')
    comment = StringField('備考')

class QuizForm(FlaskForm):
    #quiz_name = StringField('Quiz Name')
    questions = FieldList(FormField(QuestionForm), min_entries=4, max_entries=8)

class AdminReviewForm(FlaskForm):
    #quiz_name = StringField('Quiz Name')
    questions = FieldList(FormField(QuestionForm), min_entries=4, max_entries=8)


################################################################
################################################################
name='Thomas'

################################################################
################################################################
@app.route('/')
def index():
    return(render_template("basic.html",name=name))

@app.route('/questions')
def questions():
    test = Question.query.order_by(Question.id).all()

    return(render_template("questions.html",name=name,test=test))

@app.route('/questions2',methods=['GET','POST'])
def questions2():
    question = namedtuple('question', ['question_id', 'question', 'answer'])

    data = {
        'questions' : [
            question(3, 'Q 1', '100'),
            question(4, 'Q 2', '50'),
            question(5, 'Q 3', '20'),
            question(6, 'Q 4', '80'),
            question(7, 'Q 5', '10'),
            question(8, 'Q 6', '80'),
            question(9, 'Q 7', '150'),
            question(10, 'Q 8', '10'),
        ]
    }

    form = QuizForm(data=data)
    if form.validate_on_submit():
        for field in form.questions:
            print(field.question_id.data)
            print(field.question.data)
            print(field.answer.data)

        for value in form.questions.data:
            print(value)

    return render_template('questions2.html', form=form, name=name)

@app.route('/questions3',methods=['GET','POST'])
def questions3():

    question = namedtuple('question', ['question_id', 'question', 'answer'])

    question_set = []

    Quiz1 = Quiz.query.filter_by(id=1).first()
    for q1q2 in Quiz1.questions:
        question_set.append(question(q1q2.question.id, q1q2.question.question, q1q2.question.answer))

    data = {
        'questions' : question_set
    }

    form = QuizForm(data=data)
    if form.validate_on_submit():
        for field in form.questions:

            q_id = int(field.question_id.data)
            q_q = field.question.data
            q_a = field.answer.data

            Question.query.filter_by(id=q_id).first().question = q_q
            Question.query.filter_by(id=q_id).first().answer = q_a
            db.session.commit()

    return render_template('questions2.html', form=form, name=name)


@app.route('/answers')
def answers():
    test = Question.query.order_by(Question.id).all()
    return(render_template("answers.html",name=name,test=test))

@app.route('/initialize')
def initialize():

    questions = [Question(question='かようび',answer='火曜日')]
    questions.append(Question(question='ぎんこうにいく',answer='銀行に行く'))
    questions.append(Question(question='あめがふる',answer='雨がふる'))
    questions.append(Question(question='げつようび',answer='月曜日'))
    questions.append(Question(question='すいようび',answer='水曜日'))
    questions.append(Question(question='やおやにいく',answer='八百屋に行く',comment="abc"))

    for q in questions:
        q_search = Question.query.filter_by(question=q.question).first()
        if q_search == None:
            db.session.add(q)
            db.session.commit()

    Quiz1 = Quiz.query.filter_by(id=1).first()
    question_set = []

    for q1q in Quiz1.questions:
        question_set.append(q1q.question)

    return(render_template("basic.html",name=question_set))


@app.route('/admin',methods=['GET','POST'])
def admin():
    question = namedtuple('question', ['question_id', 'question', 'answer', 'comment'])

    question_set = []

    Quiz1 = Quiz.query.filter_by(id=1).first()
    for q1q2 in Quiz1.questions:
        question_set.append(question(q1q2.question.id, q1q2.question.question, q1q2.question.answer, q1q2.question.comment))

    data = {
        'questions' : question_set
    }

    form = QuizForm(data=data)
    if form.validate_on_submit():
        for field in form.questions:

            q_id = int(field.question_id.data)
            q_q = field.question.data
            q_a = field.answer.data
            q_c = field.comment.data

            Question.query.filter_by(id=q_id).first().question = q_q
            Question.query.filter_by(id=q_id).first().answer = q_a
            Question.query.filter_by(id=q_id).first().comment = q_c
            db.session.commit()

    return(render_template("admin.html", form=form))

if __name__ == '__main__':
    app.run(debug=True)
