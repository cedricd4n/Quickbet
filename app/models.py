from . import db

import datetime
from flask_login import (LoginManager, UserMixin, login_required,
                          login_user, current_user, logout_user)
from werkzeug.security import generate_password_hash, check_password_hash



class User(db.Model,UserMixin):

    id=db.Column(db.Integer,primary_key=True)
    
    email=db.Column(db.String(100),unique=True)
 
    password=db.Column(db.String(100))
    name=db.Column(db.String(1000))
    surname=db.Column(db.String(1000))
    pseudo=db.Column(db.String(1000))
    phone=db.Column(db.String(1000))
    date_n=db.Column(db.String(1000))
    phone=db.Column(db.String(1000))
    condition=db.Column(db.String(1000))
    registered_on = db.Column(db.DateTime, nullable=False)
    
    admin = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    active = db.Column(db.Boolean())
    solde= db.Column(db.Integer())
    
    compte_quickcash = db.relationship(
    'Compte_Quickcash',
    backref='user',
    lazy='dynamic'
    )
    game = db.relationship(
    'Game',
    backref='user',
    lazy='dynamic'
    )
    tmpgame= db.relationship(
    'TmpGame',
    backref='user',
    lazy='dynamic'
    )
    
    def __init__(self,email,password,name,surname,pseudo,phone,date_n,condition,confirmed,admin,active,confirmed_on=None,solde=None):

        self.email=email
        self.password=password
        self.name=name
        self.surname=surname
        self.pseudo=pseudo
        self.phone=phone
        self.date_n=date_n
        self.condition=condition
        self.solde=solde
        
        self.registered_on = datetime.datetime.now()
        self.admin=admin
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on
        self.active=active
        
    def is_admin(self):
        return self.admin

class UserAdmin(db.Model,UserMixin):
    
    id = db.Column(db.Integer(),primary_key=True)
    password=db.Column(db.String(100))
    admin = db.Column(db.Boolean, nullable=False, default=False)
     
    def __init__(self,password):
        
        self.password =password
        self.admin =False
        
    def is_admin(self):
        return self.admin    
	
    
class Compte_Quickcash(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    num_compt=db.Column(db.String(1000))
    solde= db.Column(db.Integer())
    user_id = db.Column(db.Integer(),db.ForeignKey('user.id'))
    
    def __init__(self,user_id,num_compt=None,solde=None):
        
        self.user_id =user_id
        self.num_compt=num_compt
        self.solde=solde

class Game(db.Model):
    
    id=db.Column(db.Integer(),primary_key=True)
    id_game=db.Column(db.String(1000))
    paid=db.Column(db.Integer())
    message=db.Column(db.Integer())
    user_id = db.Column(db.Integer(),db.ForeignKey('user.id'))
    statut=db.Column(db.Text())
    registered_on = db.Column(db.DateTime, nullable=False)
    
    
    def __init__(self,message,id_game,paid,user_id,statut):

        self.message=message
        self.id_game=id_game
        self.paid=paid
        self.user_id=user_id
        self.statut=statut
        self.registered_on = datetime.datetime.now()
    
       
class TmpGame(db.Model):
    
    tmp_id=db.Column(db.Integer(),primary_key=True)
    tmp_id_game=db.Column(db.String(1000))
    tmp_mise=db.Column(db.Integer())
    tmp_message=db.Column(db.Integer())
    tmp_user_id = db.Column(db.Integer(),db.ForeignKey('user.id'))
    tmp_statut=db.Column(db.Text())
    registered_on = db.Column(db.DateTime, nullable=False)
    
    
    def __init__(self,tmp_message,tmp_id_game,tmp_mise,tmp_user_id,tmp_statut):

        self.tmp_message=tmp_message
        self.tmp_id_game=tmp_id_game
        self.tmp_mise=tmp_mise
        self.tmp_user_id=tmp_user_id
        self.tmp_statut=tmp_statut
        self.registered_on = datetime.datetime.now()
      