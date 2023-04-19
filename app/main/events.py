from flask import session,jsonify
from flask_socketio import emit, join_room, leave_room
from  flask_login import login_required, login_user,logout_user,current_user
from .. import socketio,redis_store,db
from sqlalchemy import or_,and_
import random
import datetime
import shortuuid
import string
from random import choice
thread = None
file=None

x = datetime.datetime.now()
characters=''

def Password():

    
    characters=string.ascii_uppercase+x.strftime('%S%f')

    
    password="".join(choice(characters) for i in range(0,5))

    return password +'-'+shortuuid.ShortUUID().random(length=7)

def background_thread_possible():
    sets=[100,200,300,400,500,600,700,800,900,1000]
    while True:
        socketio.sleep(1)
        from app.models import TmpGame
        from .. import db
        from wsgi import app
        for paid in sets:
            with app.app_context():
                tmp_participe=TmpGame.query.filter_by(tmp_mise=paid).count()
                    
                if tmp_participe%2 ==0:
                    
                    nbr_gain=tmp_participe/2
                else:
                    nbr_gain=round(tmp_participe/2)-1
                if tmp_participe==1:
                    print("ahi")
                    possible_gain=paid+((50*paid)/100)
                    socketio.emit('possible_gain', {'mise':paid,'user_count':possible_gain,'player':1},room=str(paid),namespace='/profile')
                else:
                    user_count=round(tmp_participe/2)
                    for i in range(1,user_count+1):

                        possible_gain=round((paid*tmp_participe)/(i+1))
                        socketio.emit('possible_gain', {'mise':paid,'user_count':possible_gain,'player':nbr_gain,'players':tmp_participe},room=str(paid),namespace='/profile')
            
        
        
        
def background_thread():

    count =120
    __var__= []
    __time__=""
    
    while True:
        socketio.emit('responses',
        {'data': 'Server generated event', 'count': '','times':__time__,'status':'jouer','serie':__var__},namespace='/profile')
        socketio.sleep(10)
        var= random.sample(range(1,9),8)
        idgame=Password()
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
            {'data': 'Server generated event', 'count':int(min_sec_format),'times':timeformat,'status':'jouer','serie':var,'idgame':idgame},namespace='/profile')
            count -= 1 
            socketio.sleep(1)
                
        count =120



    
@login_required 
@socketio.on('connect', namespace='/profile')
def test_connect():
    
    from app.models import TmpGame
    from app.models import Game
    global thread
    id_room=current_user.id
    join_room(id_room)
    
   
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)   
        
        emit('my response', {'data': 'Connected', 'count': 0})
    display_hist=TmpGame.query.filter_by(tmp_user_id=current_user.id).first()
    game_participe=Game.query.filter(and_(Game.id_game==display_hist.tmp_id_game,Game.user_id==current_user.id)).first()
    print(game_participe)
    
    if display_hist is None  or game_participe is None:
       emit("room_message", f"Welcome to, {current_user.name}", room=id_room) 
    else:
       print("salut")
       socketio.emit('responses_server_third',{'data':display_hist.tmp_mise,'betnumber':display_hist.tmp_message,'idgame':display_hist.tmp_id_game},room=id_room,namespace='/profile')
       
       

@socketio.on('event_pay', namespace='/profile')
def generatedset(data):
    betnumber=data['data']
    idgame=data['tag_game']
    mises=[100,200,300,400,500,600,700,800,900,1000]
      
    socketio.emit('responses_server_first',{'data':mises,'betnumber':betnumber,'idgame':idgame},namespace='/profile')
    
  
@socketio.on('event_mise', namespace='/profile')
def generatedpossiblegain(res):
    from app.models import TmpGame
    
    mise=res['data']
    number=res['bet_number']
    id_game=res['idgame']
   
    
    statut=res['statut']
    
    global file
    if(current_user.solde<=number):
        tmpgame=TmpGame(number,id_game,mise,current_user.id,statut)
        db.session.add(tmpgame)
        db.session.commit()
        if file is None:
            file=socketio.start_background_task(target=background_thread_possible)
          
            
           
            socketio.emit('possible_gain', {'mise':mise,'user_count':5,'player':1},room=str(mise),namespace='/profile')
        socketio.emit('responses_server_second',{'data':mise,'betnumber':number,'idgame':id_game},namespace='/profile')
        
        
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
    


   
@socketio.on('event_save', namespace='/profile')
def generatedpossiblegain(res):
    
    from app.models import  Game
    mise=res['data1']
    number=res['data3']
    id_game=res['data2']
    statut="live"
    
    
    roomessage=number+mise
    game=Game(number,id_game,mise,current_user.id,statut)
    db.session.add(game)
    db.session.commit()
    
    socketio.emit('responses_server_third',{'data':mise,'betnumber':number,'idgame':id_game},room=str(roomessage),namespace='/profile')
        
        
@socketio.on('delete_row', namespace='/profile')
def delete_row(load):
    
    from app.models import TmpGame
    
    
    del_hist=TmpGame.query.filter_by(tmp_user_id=current_user.id).first()
    if del_hist is not None:
        db.session.delete(del_hist)
    
        db.session.commit()


@socketio.on("join", namespace='/profile')
def on_join(data):
    
    # session_id=request.sid
    room = data["room"]
    room_second=data["secondroom"]
    # print(f"client {current_user.name} wants to join: {room}")
    join_room(room)
    join_room(room_second)
    
    socketio.emit("room_message", f"Welcome to {room}", room=[room], namespace='/profile')  
    
   
@socketio.on('leave', namespace='/profile')
def on_leave(msg):
    
    
    room = msg["room"]
    room_second = msg["room_second"]
    # print(f"client {current_user.name} wants to leave: {room}")

   
    leave_room(room)
    leave_room(room_second)
    socketio.emit("room_message1", f"bye to {room}", namespace='/profile')


