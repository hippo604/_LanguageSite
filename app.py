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
    #questions.append(Question('かようび','火曜日'))
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

    #quiz1 = Quiz()
    #a = Association(comment = 'Association comment')
    #question1 = Question('どようび', '土曜日')
    #a.question = question1
    #quiz1.questions.append(a)
    #db.session.add_all([quiz1,a,question1])
    #db.session.commit()

    inquiz = Quiz.query.filter_by(id=1).first().questions


    return(render_template("basic.html",name=inquiz))

if __name__ == '__main__':
    app.run(debug=True)
