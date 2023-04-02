from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField,TelField,PasswordField,SelectField,BooleanField,DateField,EmailField
from wtforms.validators import DataRequired,Email,Length,Regexp,EqualTo


class RegistrationForm(FlaskForm):
    
    name = StringField('Name', validators=[DataRequired( message="Le nom ne doit pas être vide")])
    surname=StringField('Surname', validators=[DataRequired( message="Le prénom ne doit pas être vide")])
    pseudo=StringField('Pseudo',validators=[DataRequired(message="Le pseudo ne doit pas être vide"),Length(min=5, max=20 ,message="Le pseudo doit être compris entre 5 et 20 caractères."),Regexp('^(?=.*[a-z])[A-Za-z\d]{1,20}$',message="Pseudo contenant des caractères spéciaux é,@,_#...")])
    email = EmailField('Email', validators=[DataRequired(message="L'email ne doit pas être vide"), Email(message="L'email est incorrecte")])
    password = PasswordField('Password', validators=[DataRequired(message="Le mot de passe ne doit pas être vide"), Length(min=8, max=20, message="Le mot de passe doit comporter au moins huit caractères.")])
    phone=StringField('Phone',validators=[DataRequired(message="Le numéro de téléphone ne doit pas être vide"),Regexp('^(?:(?:\+|00)225[\s.-]{0,3}(?:\(0\)[\s.-]{0,3})?|0)[1-9](?:(?:[\s.-]?\d{2}){4}|\d{2}(?:[\s.-]?\d{3}){2})$',message="Le numéro de téléphone est incorrecte")])
    date=StringField('Date',validators=[DataRequired(message="La date ne doit pas être vide")])
    agree = StringField('Agree',validators=[DataRequired()])


class LoginForm(FlaskForm):
    
    
    
    email = EmailField('Email', validators=[DataRequired(message="L'email ne doit pas être vide"), Email(message="L'email est incorrecte")])
    password = PasswordField('Password', validators=[DataRequired(message="Le mot de passe ne doit pas être vide"), Length(min=8, max=20, message="Le mot de passe doit comporter au moins huit caractères.")])
   
    remember = StringField('Remember')


class ResetEmailForm(FlaskForm):
    
    email = EmailField('Email', validators=[DataRequired(message="L'email ne doit pas être vide"), Email(message="L'email est incorrecte")])


class ResetPasswordForm(FlaskForm):
    
    password = PasswordField('Password', validators=[DataRequired(message="Le mot de passe ne doit pas être vide"), Length(min=8, max=20, message="Le mot de passe doit comporter au moins huit caractères."),EqualTo('confirm_password' ,message="Les mots de passe ne correspond pas")])
   
    confirm_password=PasswordField('confirm_password', validators=[DataRequired(message="Le mot de passe  de confirmation ne doit pas être vide")])
   