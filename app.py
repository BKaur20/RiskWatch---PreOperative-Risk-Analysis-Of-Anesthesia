import flask
import pickle
import pandas as pd 
from flask import render_template, url_for, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import UserMixin, login_user, logout_user, login_required, current_user, LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
"""
from flask_wtf.csrf import CSRFProtect
"""
app = flask.Flask(__name__,template_folder='templates')
db = SQLAlchemy()
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\RiskWatch\database.db'
app.config['SECRET_KEY'] = 'qwertyuiopwertyhjklrtyuio'
"""
csrf = CSRFProtect(app)
"""
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_register'
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    mobile_no=db.Column(db.String(20),nullable=False)
    registeration_no=db.Column(db.String(40), nullable=False)

class Patient(db.Model,UserMixin):
    p_id = db.Column(db.String(10), primary_key=True)
    p_gender = db.Column(db.String(10), nullable=False)
    p_age = db.Column(db.Integer, nullable=False)
    p_bmi = db.Column(db.Integer, nullable=False)
    p_asa = db.Column(db.Integer, nullable=False)
    p_ecg = db.Column(db.String(40), nullable=False)
    p_hb = db.Column(db.Integer, nullable=False)
    p_db = db.Column(db.Integer, nullable=False)
    p_bp = db.Column(db.Integer,nullable=False)
    p_creatinine = db.Column(db.Integer,nullable=False)
    p_aptt = db.Column(db.Integer,nullable=False)
    p_result= db.Column(db.Integer,nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login_register', methods=['GET', 'POST'])
def login_register():
    if request.method == 'GET':
        return render_template('login_register.html')

    if request.method == 'POST':
        action=request.form['action']
        if request.form['action'] == 'Register':
        # Register the user
            error=None
            username = request.form['Rusername']
            password = request.form['Rpassword']
            name = request.form['name']
            email = request.form['email']
            mobile_no = request.form['mobile_no']
            registeration_no = request.form['registeration_no']
            user = Users.query.filter_by(username=username).first()
            if user:
                error = 'Username already exists'
            else: 
                hashed_password = bcrypt.generate_password_hash(password)
                new_user = Users(username=username, password=hashed_password,name=name,email=email,mobile_no=mobile_no,registeration_no=registeration_no)
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful!')
            return render_template('login_register.html',error=error,action=action)
            

        elif request.form['action'] == 'Login':
        # Login the user
            error = None
            username = request.form['Lusername']
            password = request.form['Lpassword']

            user = Users.query.filter_by(username=username).first()
            if user:
                if bcrypt.check_password_hash(user.password, password):
                    flash("You are successfully login!")
                    login_user(user)
                    return redirect(url_for('input_parameters'))

            error = "Invalid Password or username"
            return render_template('login_register.html',error=error,action=action)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))        

"""

@app.route('/login',methods = ['GET','POST'])
def login():
    if flask.request.method == 'GET':
        return(flask.render_template('login.html'))
    if flask.request.method == 'POST':
        username = flask.request.form["username"]
        password = flask.request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('input_parameters'))

        flask.flash('Invalid username or password.')
        return flask.render_template('login.html')

@app.route('/register',methods = ['GET','POST'])
def register():
    if flask.request.method == 'GET':
        return(flask.render_template('register.html'))
    if flask.request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            flask.flash('Username already exists')
            return flask.render_template('register.html')

        hashed_password = bcrypt.generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flask.flash('Registration successful!')
        return render_template('login.html')

"""
"""
class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('input_parameters'))
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)
"""

with open(f'backend/ensemble.pickle', 'rb') as f:
    model = pickle.load(f)
with open(f'backend/datapreprocessing.pickle', 'rb') as f:
    func = pickle.load(f)

@app.route('/input_parameters',methods=['GET','POST'])
@login_required

def input_parameters():
    if flask.request.method == 'GET':
        return(flask.render_template('input_parameters.html'))
    if flask.request.method == 'POST':
        patient_id=flask.request.form["patient_id"]
        gender = flask.request.form["gender"]
        age = flask.request.form["age"]
        bmi = flask.request.form["bmi"]
        asa = flask.request.form["asa"]
        preop_ecg = flask.request.form["preop_ecg"]
        preop_hb = flask.request.form["preop_hb"]
        preop_dm = flask.request.form["preop_dm"]
        preop_htn = flask.request.form["preop_htn"]
        preop_cr = flask.request.form["preop_cr"]
        preop_aptt = flask.request.form["preop_aptt"]

        input_variables = pd.DataFrame([[age, bmi, asa,preop_htn,preop_dm,preop_ecg,preop_hb,preop_aptt,preop_cr]],
                                       columns=['age', 'bmi', 'asa','preop_htn','preop_dm','preop_ecg','preop_hb','preop_aptt','preop_cr'],dtype=float
                                       )
        print(input_variables['preop_ecg'])
        input = func(input_variables)
        prediction = model.predict(input)
        prediction = prediction[0]
 
        if prediction == 1:
            prediction = 'Due'
 
        elif prediction == 2:
            prediction = 'Low'

        elif prediction == 3:
            prediction = 'Moderate'
        else:
            prediction = 'High'    

        new_patient = Patient(p_id=patient_id,p_gender=gender,p_age=age,p_bmi=bmi,p_asa=asa,p_ecg=preop_ecg,p_hb=preop_hb,p_db=preop_dm,p_bp=preop_htn,p_creatinine=preop_cr,p_aptt=preop_aptt,p_result=prediction)
        db.session.add(new_patient)
        db.session.commit()

        return flask.render_template('result.html', prediction = prediction)
    

@app.route('/patient')
def patient():
    return render_template('patient.html')

if __name__ == '__main__':
    app.run(debug=True)