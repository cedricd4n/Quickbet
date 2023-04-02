from . import auth
from flask import Blueprint,render_template,flash,redirect,url_for,request,session,jsonify
from app.forms import RegistrationForm,LoginForm,ResetEmailForm,ResetPasswordForm
from app.models import User,Compte_Quickcash
from .. import db

from werkzeug.security import generate_password_hash, check_password_hash
from  flask_login import login_required, login_user,logout_user,current_user
# from app.models import User, Game,Compte_Quickcash
from app.mail.routes import send_email

from itsdangerous import URLSafeTimedSerializer
import datetime
import shortuuid


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer('5accdb11b2c10a78d7c92c5fa102ea77fcd50c2058b00f6e')
    return serializer.dumps(email, salt='Sed0rikku')

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer('5accdb11b2c10a78d7c92c5fa102ea77fcd50c2058b00f6e')
    try:
        email = serializer.loads(
            token,
            salt='Sed0rikku',
            max_age=expiration
        )
    except:
        return False
    return email
def reset_token(token, expiration=300):
    serializer = URLSafeTimedSerializer('5accdb11b2c10a78d7c92c5fa102ea77fcd50c2058b00f6e')
    try:
        email = serializer.loads(
            token,
            salt='Sed0rikku',
            max_age=expiration
        )
    except:
        return False
    return email
@auth.route('/signup', methods=['GET','POST'])
def signup():
    errors=False
    form = RegistrationForm()
    if form.validate_on_submit():
        nom = request.form.get('name')
        prenom=request.form.get('surname')
        pseudo=request.form.get('pseudo')
        email=request.form.get('email')
        password=request.form.get('password')
        phone=request.form.get('phone')
        date=request.form.get('date')
        agree=request.form.get('agree')
        print(agree)
        useremail=User.query.filter_by(email=email).first()   
        username=User.query.filter_by(pseudo=pseudo).first()   
        userphone=User.query.filter_by(phone=phone).first()   
        if useremail or username or userphone:
            
            errors=True
            flash('Ce compte Quickcash existe déjà', 'warning')
    
        if errors:
            return redirect(url_for('auth.login'))  
        else:
            user=User(email=email, \
                        password=generate_password_hash(password,\
                        method='sha256'),name=nom,surname=prenom,pseudo=pseudo,phone=phone,date_n=date,condition=agree,confirmed=False,admin=False,active=False)
            db.session.add(user)
            db.session.commit()
            compte=Compte_Quickcash(user_id=user.id)
            db.session.add(compte)
            db.session.commit()
            token = generate_confirmation_token(user.email)
            confirm_url = url_for('auth.confirm_email', token=token, _external=True)
            html = render_template('auth/activate.html', confirm_url=confirm_url)
            subject = "Veuillez confirmer votre e-mail"
            send_email(user.email, subject, html)
            remember = True
            login_user(user,remember)
            return redirect(url_for('auth.unconfirmed'))
    
    return render_template('auth/signup.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
        
    except:
        flash("Le lien de confirmation n'est pas valide ou a expiré.," 'message')
    user = User.query.filter_by(email=email).first_or_404()   
    compte_user=Compte_Quickcash.query.filter_by(user_id=user.id).first()
    if user.confirmed:
        flash("Le compte est déjà confirmé. Veuillez vous connecter.", 'warning')
    else:
        user.confirmed = True
        user.active= True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        compte_user.num_compt=shortuuid.ShortUUID().random(length=22)
        compte_user.solde=0
        user.solde=0
        
        db.session.add(compte_user)
        db.session.commit()
        
        flash('Vous avez confirmé votre compte. Merci !', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('auth.login'))
        
        
    
   
    return render_template('auth/unconfirmed.html')

@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email=request.form.get('email')
        
        password=request.form.get('password')
        remember = True if request.form.get('agree') else False
        user=User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password,password):
            
           
            flash("le nom d'utilisateur ou le mot de passe quickcash est incorrect",'danger')
        
            return redirect(url_for('auth.login'))

        login_user(user,remember=remember)
        print('Submission successful')
        return redirect(url_for('main.profile'))
    print('Submission failed')
    return render_template('auth/login.html',form =form)



@auth.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('auth/activate.html', confirm_url=confirm_url)
    subject = "veuillez confirmer votre email"
    send_email(current_user.email, subject, html)
    
    return redirect(url_for('auth.unconfirmed'))




@auth.route('/passwordreset', methods=['GET','POST'])

def passwordreset():
    form = ResetEmailForm()
    if form.validate_on_submit():
        email=request.form.get('email')
        user=User.query.filter_by(email=email).first()
        
        if not user:
            
           
            flash("le nom d'utilisateur est incorrect",'danger')
        
            return redirect(url_for('auth.login'))
        else:
            token = generate_confirmation_token(user.email)
            password_reset_url = url_for('auth.password_reset', token=token, _external=True)
            html = render_template('auth/reset.html', password_reset_url=password_reset_url)
            subject = "Quickcash Renitialisé le mot de Passe"
            send_email(user.email, subject, html)
            print("successfull")
            flash("veuillez vérifier votre courriel pour un lien de réinitialisation du mot de passe",'success')
            return redirect(url_for('auth.login'))
    return  render_template('auth/email_confirmation.html', form=form)


@auth.route('/reset/password/<token>', methods=['GET','POST'])

def password_reset(token):
    try:
        email = reset_token(token)
        
    except:
        flash("Le lien de confirmation n'est pas valide ou a expiré.," 'message')
        return redirect(url_for('auth.login'))
    
    form=ResetPasswordForm()
    
    if form.validate_on_submit():
        password=request.form.get('password')
        print("successfull")
        try:
            user = User.query.filter_by(email=email).first_or_404()
            
        except:
            flash("le nom d'utilisateur est incorrect!", 'danger')
            return redirect(url_for('auth.login'))
        
        user.password=generate_password_hash(password,method='sha256')
        
        db.session.add(user)
        db.session.commit()
        flash("votre mot de passe a été mis à jour",'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/password.html',token=token,form=form)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():

    logout_user()
    return redirect(url_for('main.index'))  