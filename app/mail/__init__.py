from flask import render_template, Blueprint

mails=Blueprint('mails',__name__,template_folder='templates',static_folder='static')


from . import routes