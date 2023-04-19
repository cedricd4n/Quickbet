#!/bin/env python
from app import app, socketio,db

app = app(debug=True)

if __name__ == '__main__':
   with app.app_context():
        db.create_all()
        
        socketio.run(app)
