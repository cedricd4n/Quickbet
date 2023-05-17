from flask import render_template, Blueprint,render_template,flash,redirect,url_for,request,session,jsonify,abort
from app.models import *
from app.forms import *
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.base import AdminIndexView, expose
from .. import db,admin
from . import admin_bp


@admin_bp.route('/login', methods=['GET','POST'])
def login():
    next = "/admin"
    form = AdminLoginForm()
    if form.validate_on_submit():
        
        password=request.form.get('password')
        
        if password==".Qu1ckc@sh":
            session['logged_in']= True
            return redirect(next)
        
        else:
                flash('Wrong email or password', 'error-message')
    else:
        next = request.args.get('next')           
    return render_template("admin/login.html", form=form, next=next)            

class SecureViewModel(ModelView):
    
    
    
    def is_accessible(self):
        if "logged_in" in session:
            
            return True
        else:
            abort(403)
@admin_bp.route('/logout', methods=['GET','POST'])         
def logout():
    form = AdminLoginForm()

    if form.validate_on_submit():
        password=request.form.get('password')
        
        if password==".Qu1ckc@sh":
            session.clear()
            
            return redirect("/")

        

    return render_template("admin/logout.html", form=form)
                
    
     
admin.add_view(SecureViewModel(User,db.session))
admin.add_view(SecureViewModel(UserAdmin,db.session))
admin.add_view(SecureViewModel(Compte_Quickcash,db.session))
admin.add_view(SecureViewModel(Game,db.session))
admin.add_view(SecureViewModel(TmpGame,db.session))