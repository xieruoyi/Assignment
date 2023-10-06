from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

def email_format(form, field):
    if "@" not in field.data:
        raise ValidationError("Please include an @ in the email address.'{}' is missing an '@'.".format(field.data))
    

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT email address?', validators=[DataRequired(), email_format])
    submit = SubmitField('Submit')



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        old_email = session.get('email')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
        session['email'] = form.email.data
        session['notutmail'] = False 
        substring = 'utoronto'
        if substring not in form.email.data:
            session['notutmail'] = True
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'),notutmail = session.get('notutmail'))

# @app.route('/user/<name>')
# def user(name):
#     return render_template('user.html',name = name, cur)
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/clear')
def clear_session_data():
    session.clear()
    return redirect(url_for(index))