import json
import logging
# from blueprint_basket.route import blueprint_basket
from blueprint_basket.route import blueprint_order
from blueprint_report.route import blueprint_report
from flask import Flask, render_template, session, redirect, url_for
from blueprint_query.route import blueprint_query
from authentication_blueprint.access import authentication_blueprint, login_required


#новое
app = Flask(__name__)
with open('data_files/dbconfig.json') as f:
    app.config['dbconfig'] = json.load(f)
    # dbconfig = json.load(f)
with open('authentication_blueprint/access.json') as f:
    app.config['access_config'] = json.load(f)

#новое
app.register_blueprint(blueprint_query, url_prefix = '/query')
app.register_blueprint(authentication_blueprint, url_prefix = '/auth')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_order, url_prefix='/order')
app.secret_key = 'you will never guess'




@app.route('/', methods=['GET', 'POST'])
@login_required
def menu_choice():
    # if 'user_id' in session:
    if session.get('user_group') == None or session.get('user_group') == "ordinary":
        session['user_group'] = "ordinary"
        return render_template('external_user_menu.html')
    elif session.get('user_group') == "manager":
        return render_template('manager_menu.html')
    else:
        return render_template('director_menu.html')





@app.route('/exit')
def query_func():
    session.clear()
    return redirect(url_for('auth_bp.auth_index'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)

# СТОП
