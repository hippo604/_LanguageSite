from langsite import app,db
from langsite.models.models import Question
from flask import render_template

name='Mark'

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
    q1 = Question('きんようび','金曜日')
    q2 = Question('ぎんこうにいく','銀行に行く')
    q3 = Question('あめがふる','雨がふる')
    db.session.add_all([q1,q2,q3])
    db.session.commit()
    return(render_template("basic.html",name=name))

if __name__ == '__main__':
    app.run(debug=True)
