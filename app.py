from langsite import app,db
from langsite.models.models import Question,QuizStatusEnum,Quiz,Association
from flask import render_template

name='Thomas'

@app.route('/')
def index():
    return(render_template("basic.html",name=name))

@app.route('/questions')
def questions():
    test = Question.query.order_by(Question.id).all()

    return(render_template("questions.html",name=name,test=test))

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


@app.route('/admin')
def admin():
    #...
    return(render_template("admin.html"))

if __name__ == '__main__':
    app.run(debug=True)
