from functools import wraps
from flask import session, current_app, request, Blueprint, redirect, url_for, render_template
from work_with_db import select_dict
import logging
logging.basicConfig(level=logging.DEBUG)

authentication_blueprint = Blueprint('auth_bp', __name__, template_folder = 'templates')

def find_userid(login, password, user_dict):
    for user in user_dict:
        if user['login'] == login and user['password'] == password:
            return user['userid'], user['group']
    return None, None

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        return redirect(url_for('auth_bp.auth_index'))
    return wrapper

def group_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            user_group = session.get('user_group')
            if user_group:
                access = current_app.config['access_config'] #глобальная переменная
                user_target = request.blueprint
                if user_group in access and user_target in access[user_group]:
                    return func(*args, **kwargs)
                else:
                    return 'у вас нет доступа к этому функцианалу'
            else:
                return 'Только для внутренних пользователей'
        else:
            #return 'Вам необходимо авторизоваться!'
            session['previous_url'] = request.referrer
            return redirect(url_for('auth_bp.auth_index'))
    return wrapper

@authentication_blueprint.route('/', methods = ['GET', 'POST'])
def auth_index():
    previous_url = session.get('previous_url')
    print(previous_url)

    if request.method == 'GET':
        return render_template("auth_form.html")
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        if not login or not password:
            logging.error("Empty login or password field.")
            return render_template("auth_form.html", error_message = 'пустое поле')
        else:
            _sql = 'select * from users'
            users = select_dict(current_app.config['dbconfig'], _sql)
            print(users)

            userid, user_group = find_userid(login, password, users)
            if userid is not None:
                session['user_id'] = userid
                session['user_group'] = user_group
                print(f"User {login} successfully logged in. UserID: {userid}, Group: {user_group}")
                #session.pop('previous_url', None)
                if previous_url is None:
                    previous_url = '/'
                    redirect(url_for('bp_query.start_index'))
                return redirect(previous_url)
            else:

                _sql = 'select * from ext_users'
                users = select_dict(current_app.config['dbconfig'], _sql)
                print(users)
                userid, user_group = find_userid(login, password, users)
                if userid:
                    session['user_id'] = userid
                    session['user_group'] = user_group
                    # session.pop('previous_url', None)
                    if previous_url is None:
                        previous_url = '/'
                        redirect(url_for('bp_query.start_index'))
                    return redirect(previous_url)
                else:
                    return render_template("auth_form.html", error_message='Неверный логин/пароль')
                #конец
                # print(f"Failed login attempt for user {login}")
                # return render_template("auth_form.html", error_message='неверный логин/пароль')


@authentication_blueprint.route('/lk', methods = ['GET', 'POST'])
@login_required
def lk_index():
    if 'user_id' in session:
        user_group = session.get('user_group')
    return render_template('lk.html', user_group = user_group)



# @authentication_blueprint.route('/lk', methods = ['GET', 'POST'])
# @login_required
# def lk_index():
#     if 'user_id' in session:
#         user_group = session.get('user_group')
#         print(f"User in session. UserID: {session['user_id']}, Group: {user_group}")
#     else:
#         print("No user in session")
#     return render_template('lk.html', user_group = user_group)