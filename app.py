from langsite import app,db
from langsite.models.models import Question,QuizStatusEnum,Quiz,Association,Setting
from flask import render_template, url_for
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
    question_image = StringField('質問の画像')
    answer = StringField('答え')
    answer_image = StringField('答えの画像')
    result= StringField('結果')
    result_comment= StringField('コメント')

#Multi-line form for the quiz (no answers)
class QuizForm(FlaskForm):
    questions = FieldList(FormField(QuestionForm), min_entries=0, max_entries=8)

#Multi-line form for the quiz (includes answers)
class QuizAnswerForm(FlaskForm):
    questions = FieldList(FormField(AnswerForm), min_entries=0, max_entries=14)

#Single line for the admin page
class AdminQuestionForm(Form):
    question_id = StringField('ID')
    question = StringField('質問')
    question_image = StringField('質問の画像')
    answer = StringField('答え')
    answer_image = StringField('答えの画像')
    result = StringField('結果')
    comment = StringField('備考')
    result_comment = StringField('コメント')

#Multi-line form for the admin page
class AdminReviewForm(FlaskForm):
    #quiz_name = StringField('Quiz Name')
    questions = FieldList(FormField(AdminQuestionForm), min_entries=3, max_entries=8)

class SettingForm(FlaskForm):
    name = StringField('名前')
    default_quiz = StringField('次のクイズ')


def refresh():
    global name
    name=Setting.query.filter_by(key="name").first().value
    global default_quiz
    default_quiz = int(Setting.query.filter_by(key="default_quiz").first().value)

refresh()

@app.route('/')
def index():

    refresh()
    return(render_template("basic.html",name=name))


@app.route('/questions',methods=['GET','POST'])
def questions():

    refresh()
    question = namedtuple('question', ['question_id', 'question', 'question_image'])

    question_set = []

    Quiz1 = Quiz.query.filter_by(id=default_quiz).first()
    for q1q2 in Quiz1.questions:

        question_image = q1q2.question.question_image

        if question_image != None:
            questionimagelink = url_for('static', filename='images/' + question_image)
        else:
            questionimagelink = None

        question_set.append(question(q1q2.question.id, q1q2.question.question, questionimagelink))


    return render_template('questions3.html', question_set=question_set, name=name)


@app.route('/answers',methods=['GET','POST'])
def answers():
        refresh()
        question = namedtuple('question', ['question_id', 'question', 'question_image', 'answer', 'answer_image', 'result', 'result_comment'])

        question_set = []

        Quiz1 = Quiz.query.filter_by(id=default_quiz).first()

        for q1q2 in Quiz1.questions:
            question_set.append(question(q1q2.question.id, q1q2.question.question, q1q2.question.question_image, q1q2.question.answer, q1q2.question.answer_image, q1q2.result, q1q2.result_comment))

        data = {
            'questions' : question_set
        }

        print("**************BEGINNING of question set: " )
        print(question_set)
        print("**************END of question set: " )


        form = QuizAnswerForm(data=data)
        if form.validate_on_submit():
            for field in form.questions:
                try:
                    q_id = int(field.question_id.data)
                    # print("app.py answers attempt to determine q_id")
                except ValueError:
                    pass

                q_r = field.result.data
                q_rc = field.result_comment.data

                Quiz1 = Quiz.query.filter_by(id=default_quiz).first()

                # Convoluted iteration through Association objects.
                for q1q2 in Quiz1.questions:
                    print("q1q2.question.id: " + str(q1q2.question.id) + "; q_id=" + str(q_id))
                    if q1q2.question.id == q_id:
                        q1q2.result = q_r
                        q1q2.result_comment = q_rc
                        print("**************BEGINNING of result and comment: " )
                        print("result: " + q_r)
                        print("result: " + q_rc)
                        print("**************END of question set: " )

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

@app.route('/init_settings')
def init_settings():
    settings = [Setting(key='name', value="Emily")]
    settings.append(Setting(key='default_quiz', value='0'))

    for s in settings:
        s_search = Setting.query.filter_by(key=s.key).first()
        if s_search == None:
            db.session.add(s)
            db.session.commit()

    return(render_template("basic.html",name="Em"))



@app.route('/admin',methods=['GET','POST'], defaults={'quiz_number': default_quiz})
@app.route('/admin/<quiz_number>',methods=['GET','POST'])
def admin(quiz_number):
    refresh()

    question = namedtuple('question', ['question_id', 'question', 'question_image', 'answer', 'answer_image', 'result', 'comment', 'result_comment'])

    question_set = []

    Quiz1 = Quiz.query.filter_by(id=int(quiz_number)).first()
    for q1q2 in Quiz1.questions:
        question_set.append(question(q1q2.question.id, q1q2.question.question, q1q2.question.question_image, q1q2.question.answer, q1q2.question.answer_image, q1q2.result, q1q2.question.comment, q1q2.result_comment))

    data = {
        'questions' : question_set
    }

    form = AdminReviewForm(data=data)

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

@app.route('/settings',methods=['GET','POST'])
def settings():

    refresh()
    # name = Setting.query.get_or_404("Name")
    # name = Setting.query.filter_by(key="name").first().value
    # def_quiz = Setting.query.filter_by(key="default_quiz").first().value

    return(render_template("settings.html", name=name))






if __name__ == '__main__':
    app.run(debug=True)
