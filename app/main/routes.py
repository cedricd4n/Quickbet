from flask import Blueprint,render_template,flash,request,redirect,url_for,session,jsonify,abort
from . import main
from app.models import User,Compte_Quickcash,Game
from app.forms import RegistrationForm
from app.decorators import check_confirmed
from  flask_login import login_required, login_user,logout_user,current_user
from datetime import datetime

def Paid():
    paid_tab=[]

    start=100
    step=100
    while start<=10000:
        paid_tab.append(start)
        if start==1000:
            step=200 

        if start==4000:

            step=500    
        if start==6000:

            step=1000 
        start+=step
    return paid_tab
@main.route('/')
def index():
   
    form = RegistrationForm()
    #print(form.csrf_token)
    return render_template('auth/signup.html', form=form)
        # return redirect(url_for('auth.signup'))
    # form = LoginForm()
    # if form.validate_on_submit():
    #     session['name'] = form.name.data
    #     session['room'] = form.room.data
    #     return redirect(url_for('.chat'))
    # elif request.method == 'GET':
    #     form.name.data = session.get('name', '')
    #     form.room.data = session.get('room', '')
    # return render_template('main/gochat.html', form=form)


@main.route('/profile')
@login_required
@check_confirmed
def profile():
    user = User.query.filter_by(id=current_user.id).first()   
    compte_user=Compte_Quickcash.query.filter_by(user_id=user.id).first()
    numero_client=compte_user.num_compt
    paids=Paid()
    game=Game.query.order_by(Game.id.desc()).filter_by(user_id=user.id).first()
    if game is not None:
        
        print(game)
        numero_jeu=game.id_game
        date_jeu=game.registered_on
        dt=datetime.fromisoformat(str(date_jeu))
        formatted_data=dt.strftime('%d/%m/%Y à %H:%M')
        mise_jeu=game.paid
        numero_parier=game.message
        statut=game.statut
    
    else:
        numero_jeu='pas information'
        # date_jeu=game.registered_on
        # dt=datetime.fromisoformat(str(date_jeu))
        formatted_data='pas information'
        mise_jeu='pas information'
        numero_parier='pas information'
        statut='pas information'
        
    
    return render_template('main/profile.html',paids=paids,numero_client=numero_client,numero_jeu=numero_jeu,formatted_data=formatted_data,mise_jeu=mise_jeu,numero_parier=numero_parier,statut=statut)


@main.route('/terms')
def terms():
    
        return render_template('main/terms&use.html') 
    


@main.route('/quickcash/historique')
def historique():
    
    
    return "hello world" 
    