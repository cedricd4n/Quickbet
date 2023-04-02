from flask import session,jsonify
from flask_socketio import emit, join_room, leave_room
from  flask_login import login_required, login_user,logout_user,current_user
from .. import socketio,redis_store
import random
import datetime
import shortuuid
import string
from random import choice
thread = None

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
    
    while True:
        socketio.emit('game',
        {'data': 'Server generated event', 'count': count,'times':__time__,'status':'jouer','serie':__var__},namespace='/profile')
        socketio.sleep(10)
        var= random.sample(range(1,9),8)
        idgame=Password()
        while  count:
            mins, secs = divmod(count, 60)
            min_sec_format = '{:02d}:{:02d}'.format(mins, secs)
            if mins!=0:
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                min_sec_format = '{:02d}'.format((mins*60)+secs)
            else:
                min_sec_format = '{:02d}'.format(secs)
                timeformat = '{:02d}s restant'.format((mins*60)+secs)
        
        
            socketio.emit('game',
            {'data': 'Server generated event', 'count':int(min_sec_format),'times':timeformat,'status':'jouer','serie':var,'idgame':idgame},namespace='/profile')
            socketio.sleep(1)
            count = count-1
        count =120


@login_required 
@socketio.on('connect', namespace='/profile')
def test_connect():

    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)
    # emit('my response', {'data': 'Connected', 'count': 0})
@login_required   
@socketio.on('client_response', namespace='/profile')
def sendmessage(data):
    var= random.sample(range(1,9),8)
    
    data_numero=int(data["data_numero"])
    data_mise=int(data["data_mise"])
    if data_numero in var:
        
        
        if (current_user.solde<=data_mise):
            
    
            socketio.emit('server_response',{'data':current_user.solde},namespace='/profile')
    

@login_required 
@socketio.on("join", namespace='/profile')
def on_join(data):
    
    # session_id=request.sid
    room = data["room"]
    room_second=data["room_second"]
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
