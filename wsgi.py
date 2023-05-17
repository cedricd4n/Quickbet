#!/bin/env python
from app import create_app, socketio,db
from flask import session,jsonify
from flask_socketio import emit, join_room, leave_room
from  flask_login import login_required, login_user,logout_user,current_user

from sqlalchemy import or_,and_

import random
import datetime
# from datetime import datetime
import shortuuid
import string
from random import choice
app = create_app(debug=True)

thread = None
file=None

x = datetime.datetime.now()
characters=''

def Password():

    
    characters=string.ascii_uppercase+x.strftime('%S%f')

    
    password="".join(choice(characters) for i in range(0,5))

    return password +'-'+shortuuid.ShortUUID().random(length=7)

 
def background_thread():

    count =120
    __var__= []
    __time__=""
    id_game=""
    while True:
        
        keys=[]
        val=[]
        k=[]
        v=[]
        salle=0
        dictionary={}
        payement=0
        dictionary={}
        payement=0
        payement_admin=0
        
       
        
        from app.models import Game
        from app.models import User
        from app.models import Compte_Quickcash
      
        mises=[100,200,300,400,500,600,700,800,900,1000]
        if id_game!="":
            for paid in mises:
                     with app.app_context():
                        game_participe=Game.query.filter(and_(Game.id_game==code_game,Game.paid==paid)).count()
                        print(game_participe)
                        if  game_participe!=0:
                            for i in range(1,9):
                                result = Game.query.filter(and_(Game.message==i,Game.id_game==code_game,Game.paid==paid)).count()
                                if result!=0 and result!=game_participe:
                                        keys.append(str(i))
                                        cnt=result
                                        val.append(cnt)
                                if  result!=0 and result==game_participe:
                                        keys.append(str(i))
                                        cnt=result
                                        val.append(cnt)
                            print(keys)
                            print(val) 
                            for key, value in zip(keys,val):

                                dictionary[key]=value 
                            z=len(val)
                            print(z)
                            if z!=1 and len(val) != 0:
                                a=[]
                            
                                compt=min(val)  
                                
                                for k,v in dictionary.items():
                                    if  compt==v:
                                        a.append(int(k))
                                        break
                                
                                compt=min(a)   
                                
                                print(len(a))
                                print("bleu")
                                print(str(compt))
                                for i in keys:
                                    
                                    if str(compt)==i:
                                        print("vous avez gagné le jeu",str(compt))
                                        Game.query.filter(and_(Game.message==compt,Game.id_game==code_game,Game.paid==paid)).update({
                                                    'statut': 'Gagné'
                                                    })
                                        db.session.commit()
                                        results = Game.query.filter(and_(Game.message==compt,Game.id_game==code_game,Game.paid==paid)).all()
                                        results_nbr = Game.query.filter(and_(Game.message==compt,Game.id_game==code_game,Game.paid==paid)).count()
                                        payement=round(((paid*game_participe)/(results_nbr+1)))
                                        #ajouter le paiement de l' admin
                                        for results in results:
                                            User.query.filter_by(id=results.user_id).update({
                                                    'solde': (User.solde+payement)
                                                    })
                                            db.session.commit()
                                        salle=compt+paid
                                        
                                        socketio.emit('server_resultat_win', {'statut':'Gagné'},room=str(salle))
                                    else:
                                        Game.query.filter(and_(Game.message==i,Game.id_game==code_game,Game.paid==paid)).update({
                                                    'statut': 'Perdu'
                                                })
                                        db.session.commit()
                                        
                                        salle_lost=int(i)+paid
                                        socketio.emit('server_resultat_lose', {'statut':str(compt)+' le numero gagnant (perdu)'}, room=str(salle_lost))
                                        print("vous avez perdu le jeu",i,str(compt))
                            elif z==1 and len(val) != 0:
                                compt=random.randint(1,8)
                                
                                if compt!=int(keys[0]):
                                    payement_admin=paid*game_participe
                                    #ajouter paiement admin
                                    Game.query.filter(and_(Game.message==int(keys[0]),Game.id_game==code_game,Game.paid==paid)).update({
                                                    'statut': 'Perdu'
                                                    })
                                    db.session.commit()
                                    
                                    n=str(compt)+' est le numero gagnant (perdu)'
                                    
                                    salle=int(keys[0])+paid
                                    print("vert")
                                    # print(f,r,n)
                                    socketio.emit('server_resultat_lose', {'statut':n},room=str(salle)) 
                                    
                                else:
                                    payement_admin=paid*game_participe
                                    Game.query.filter(and_(Game.message==int(keys[0]),Game.id_game==code_game,Game.paid==paid)).update({
                                                    'statut': 'Perdu'
                                                    })
                                    db.session.commit()
                                    
                                    r=int(keys[0])+1
                                    salle=int(keys[0])+paid
                                    print("rouge")
                                    # print("vous avez perdu le jeu",r,keys[0])
                                    socketio.emit('server_resultat_lose', {'statut':str(r)+' le numero gagnant (perdu)'}, room=str(salle))               
                            keys=[]
                            val=[]  
                            dictionary={}
                            compt=0
                            salle=[]  
        socketio.emit('responses',
        {'data': 'Server generated event', 'count': '','times':__time__,'status':'jouer','serie':__var__})
        socketio.sleep(10)
        var= random.sample(range(1,9),8)
        code_game=Password()
        while  count>=0:
            mins, secs = divmod(count, 60)
            min_sec_format = '{:02d}:{:02d}'.format(mins, secs)
            if mins!=0:
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                min_sec_format = '{:02d}'.format((mins*60)+secs)
            else:
                min_sec_format = '{:02d}'.format((mins*60)+secs)
                timeformat = '{:02d}s'.format((mins*60)+secs)
            socketio.emit('responses_server',
            {'data': 'Server generated event', 'count':int(min_sec_format),'times':timeformat,'status':'jouer','serie':var,'idgame':code_game})
            socketio.sleep(1)
            
            count -= 1 
            
        count =120
        id_game=code_game   
             
        





    
@login_required 
@socketio.on('connect')
def test_connect():
    
    from app.models import TmpGame
    from app.models import Game
    global thread
    id_room=current_user.id
    join_room(id_room)
    
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)
           
        
      
        
    emit('my response', {'data': 'Connected', 'count': 0})
    
    if  Game.query.count()==0 or TmpGame.query.count()==0:
         emit("room_message", f"Welcome to, {current_user.name}", room=id_room) 
    else:
        
        display_hist=TmpGame.query.order_by(TmpGame.tmp_id.desc()).filter_by(tmp_user_id=current_user.id).first()
        if display_hist is None:
            emit("room_message", f"Welcome to, {current_user.name}", room=id_room) 
        
        else:
            
            game_participe=Game.query.filter(and_(Game.id_game==display_hist.tmp_id_game,Game.user_id==current_user.id)).first()
            if game_participe is None:
                emit("room_message", f"Welcome to, {current_user.name}", room=id_room)    
            else:
                print("salut")
                socketio.emit('responses_server_third',{'data':display_hist.tmp_mise,'betnumber':display_hist.tmp_message,'idgame':display_hist.tmp_id_game},room=id_room)
                tmp_participe=TmpGame.query.filter(TmpGame.tmp_mise==display_hist.tmp_mise).count()
                
                if tmp_participe%2 ==0:
                    
                    nbr_gain=tmp_participe/2
                else:
                    nbr_gain=round(tmp_participe/2)-1
                if tmp_participe==1:
                    print("ahi")
                    possible_gain=display_hist.tmp_mise+((50*display_hist.tmp_mise)/100)
                    socketio.emit('possible_gain', {'mise':display_hist.tmp_mise,'user_count':possible_gain,'player':1},room=id_room)
                else:
                    user_count=round(tmp_participe/2)
                    for i in range(1,user_count+1):

                        possible_gain=round((display_hist.tmp_mise*tmp_participe)/(i+1))
                        socketio.emit('possible_gain', {'mise':display_hist.tmp_mise,'user_count':possible_gain,'player':nbr_gain,'players':tmp_participe},room=id_room)
            
        

@socketio.on('event_pay')
def generatedset(data):
    betnumber=data['data']
    idgame=data['tag_game']
    room_user=current_user.id
    mises=[100,200,300,400,500,600,700,800,900,1000]
      
    socketio.emit('responses_server_first',{'data':mises,'betnumber':betnumber,'idgame':idgame},room=room_user)
    
  
@socketio.on('event_mise')
def generatedpossiblegain(res):
    from app.models import TmpGame
    
    mise=res['data']
    number=res['bet_number']
    id_game=res['idgame']
   
    room_user=current_user.id
    statut=res['statut']
    

    if(current_user.solde<=number):
        del_doublon=TmpGame.query.filter_by(tmp_user_id=current_user.id).first()
        if del_doublon is not None:
          
            db.session.delete(del_doublon)
    
            db.session.commit()
            tmpgame=TmpGame(number,id_game,mise,current_user.id,statut)
            db.session.add(tmpgame)
            db.session.commit()
        else:    
            tmpgame=TmpGame(number,id_game,mise,current_user.id,statut)
            db.session.add(tmpgame)
            db.session.commit()
        
        tmp_participe=TmpGame.query.filter(TmpGame.tmp_mise==mise).count()
        print(tmp_participe)    
        if tmp_participe%2 ==0:
            
            nbr_gain=tmp_participe/2
        else:
            nbr_gain=round(tmp_participe/2)-1
        if tmp_participe==1:
            print("good")
            possible_gain=mise+((50*mise)/100)
            socketio.emit('possible_gain', {'mise':mise,'user_count':possible_gain,'player':1},room=str(mise))
        else:
            user_count=round(tmp_participe/2)
            for i in range(1,user_count+1):

                possible_gain=round((mise*tmp_participe)/(i+1))
                socketio.emit('possible_gain', {'mise':mise,'user_count':possible_gain,'player':nbr_gain,'players':tmp_participe},room=str(mise))
    
        socketio.emit('responses_server_second',{'data':mise,'betnumber':number,'idgame':id_game},room=room_user)
        
        
    # else:
    #     socketio.emit('warning_response', {'data': 'Rechargez votre compte pour ce paris'},room=customer,namespace='/profile')
    
   
   
       
# #     var= random.sample(range(1,9),8)
    
# #     data_numero=int(data["data_numero"])
# #     data_mise=int(data["data_mise"])
# #     if data_numero in var:
        
        
# #         if (current_user.solde<=data_mise):
            
    
# #             socketio.emit('server_response',{'data':current_user.solde},namespace='/profile')
    
    



#     # else:
#     #     socketio.emit('warning_response', {'data': 'Rechargez votre compte pour ce paris'},room=customer,namespace='/profile')
    
   
   
       
# #     var= random.sample(range(1,9),8)
    
# #     data_numero=int(data["data_numero"])
# #     data_mise=int(data["data_mise"])
# #     if data_numero in var:
        
        
# #         if (current_user.solde<=data_mise):
            
    
# #             socketio.emit('server_response',{'data':current_user.solde},namespace='/profile')
    


   
@socketio.on('event_save')
def generatedpossiblegain(res):
    
    from app.models import  Game
    from app.models import User
    from app.models import Compte_Quickcash
    mise=res['data1']
    number=res['data3']
    id_game=res['data2']
    statut="live"
    
    
    roomessage=number+mise
    game=Game(number,id_game,mise,current_user.id,statut)
    db.session.add(game)
    db.session.commit()
    User.query.filter_by(id=current_user.id).update({
    'solde': (current_user.solde-mise)
    })
    data_solde=Compte_Quickcash.query.filter_by(user_id=current_user.id).first()
    Compte_Quickcash.query.filter_by(user_id=current_user.id).update({
    'solde': (data_solde.solde-mise)
    })
    db.session.commit()
    data_solde=Compte_Quickcash.query.filter_by(user_id=current_user.id).first()
    socketio.emit('responses_server_third',{'data':mise,'betnumber':number,'idgame':id_game},room=str(roomessage))
    socketio.emit('server_response_solde',{'data':data_solde.solde},room=str(roomessage))
    game=Game.query.order_by(Game.id.desc()).filter_by(user_id=current_user.id).first()
    numero_jeu=game.id_game
    date_jeu=game.registered_on
    dt=datetime.datetime.fromisoformat(str(date_jeu))
    formatted_data=dt.strftime('%d/%m/%Y à %H:%M')
    mise_jeu=game.paid
    numero_parier=game.message
    statut=game.statut    
    socketio.emit('detail_jeu',{'numero_jeu': numero_jeu,'formatted_data':formatted_data,'mise_jeu':mise_jeu,'numero_parier':numero_parier,'statut':statut},room=str(roomessage)) 
       
@socketio.on('delete_row')
def delete_row(load):
    
    from app.models import TmpGame
    
    
    TmpGame.query.filter_by(tmp_user_id=current_user.id).delete()
    # if del_hist is not None:
    #     db.session.delete(del_hist)
    
    db.session.commit()

@socketio.on("join")
def on_join(data):
    
    # session_id=request.sid
    room72=data['room72']
    room = data["room"]
    room_second=data["secondroom"]
    # print(f"client {current_user.name} wants to join: {room}")
    join_room(room)
    join_room(room_second)
    join_room(room72)
    
    socketio.emit("room_message", f"Welcome to {room}", room=[room])  
    
   
@socketio.on('leave')
def on_leave(msg):
    
    
    room = msg["room"]
    room_second = msg["room_second"]
    # print(f"client {current_user.name} wants to leave: {room}")

   
    leave_room(room)
    leave_room(room_second)
    socketio.emit("room_message1", f"bye to {room}")




if __name__ == '__main__':
   with app.app_context():
        db.create_all()
        
        socketio.run(app)
