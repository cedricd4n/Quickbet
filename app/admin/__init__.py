from flask import render_template, Blueprint

admin_bp=Blueprint('admin_bp',__name__,url_prefix='/admin',template_folder='templates',static_folder='static')


from . import routes