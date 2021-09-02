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

#Single line for the quiz (questions only)
class QuestionForm(Form):
    question_id = StringField('ID')
    question = StringField('質問')
    answer = StringField('答え')
    comment = StringField('備考')

#Single line for the quiz (includes answers only)
class AnswerForm(Form):
    question_id = StringField('ID')
    question = StringField('質問')
    answer = StringField('答え')
    result= StringField('結果')

#Multi-line form for the quiz (no answers)
class QuizForm(FlaskForm):
    questions = FieldList(FormField(QuestionForm), min_entries=4, max_entries=8)

#Multi-line form for the quiz (includes answers)
class QuizAnswerForm(FlaskForm):
    questions = FieldList(FormField(AnswerForm), min_entries=4, max_entries=8)

#Multi-line form for the admin page
class AdminReviewForm(FlaskForm):
    #quiz_name = StringField('Quiz Name')
    questions = FieldList(FormField(QuestionForm), min_entries=4, max_entries=8)

################################################################
name='Thomas'


################################################################
@app.route('/')
def index():
    return(render_template("basic.html",name=name))


@app.route('/questions',methods=['GET','POST'])
def questions():

    question = namedtuple('question', ['question_id', 'question'])

    question_set = []

    Quiz1 = Quiz.query.filter_by(id=1).first()
    for q1q2 in Quiz1.questions:
        question_set.append(question(q1q2.question.id, q1q2.question.question))

    return render_template('questions3.html', question_set=question_set, name=name)


@app.route('/answers',methods=['GET','POST'])
def answers():
        question = namedtuple('question', ['question_id', 'question', 'answer', 'result'])

        #Start blank list
        question_set = []

        Quiz1 = Quiz.query.filter_by(id=1).first()

        for q1q2 in Quiz1.questions:
            question_set.append(question(q1q2.question.id, q1q2.question.question, q1q2.question.answer, q1q2.result))

        data = {
            'questions' : question_set
        }

        form = QuizAnswerForm(data=data)
        if form.validate_on_submit():
            for field in form.questions:

                try:
                    q_id = int(field.question_id.data)
                    print("app.py answers attempt to determine q_id")
                except ValueError:
                    pass

                q_r = field.result.data

                Quiz1 = Quiz.query.filter_by(id=1).first()

                # Convoluted iteration through Association objects.
                for q1q2 in Quiz1.questions:
                    if q1q2.question.id == q_id:
                        q1q2.result = q_r

                db.session.commit()

                q_id = None

        return render_template('answers2.html', form=form, name=name)

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

    return(render_template("basic.html",name=name))

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

            #Need to make sure blank rows don't make it into the db
            try:
                q_id = int(field.question_id.data)
            except ValueError:
                pass

            # Capturing items in Quick field
            q_q = field.question.data
            q_a = field.answer.data
            q_c = field.comment.data

            try:
                question_assembled = Question.query.filter_by(id=q_id).first()
            except ValueError:
                pass

            if question_assembled != None and q_id != "" and q_q != "" and q_a != "":
                question_assembled.question = q_q
                question_assembled.answer = q_a
                question_assembled.comment = q_c

            #Don't want question_assembled bleeding into the next iteration
            question_assembled = None

        db.session.commit()

    return(render_template("admin.html", form=form, name=name))

if __name__ == '__main__':
    app.run(debug=True)
