import os
from authentication_blueprint.access import *
from flask import *
from DBcm import *
from work_with_db import *
from sql_provider import *
from datetime import datetime


blueprint_order = Blueprint('bp_order', __name__, template_folder='templates', static_folder='static')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@blueprint_order.route('/start')
@group_required
@login_required
def start():
    if 'basket' not in session.keys():
        print('!')
        session['basket'] = {}
    return redirect(url_for('bp_order.choose'))





@blueprint_order.route('/', methods=['GET', 'POST'])
@login_required
def choose():
    dbconfig = current_app.config['dbconfig']

    # Проверяем наличие ключа 'basket' в объекте session
    basket = session.get('basket', {})

    if request.method == 'GET':
        sql = provider.get('all_items.sql')
        items = select_dict(dbconfig, sql)
        print("SQL Query:", sql)  # Добавьте эту строку
        print("basket", basket)
        print("items", items)
        return render_template('basket_show.html', item=items, basket=basket,
                               bask_keys=basket.keys())
    else:
        id_product = request.form.get('pr_id')
        print(id_product)
        sql = provider.get('add_item.sql', id=id_product)
        print("SQL Query:", sql)  # Добавьте эту строку

        item = select_dict(dbconfig, sql)[0]
        print('\n')
        print(item)
        add_to_basket(basket, item)
        if not session.modified:
            session.modified = True
        return redirect(url_for('bp_order.choose'))



def add_to_basket(bask, item):
    if str(item['pr_id']) in bask.keys():
        bask[str(item['pr_id'])]['amount'] += 1
        print("Basket", bask)
    else:
        bask[str(item['pr_id'])] = {'pr_name': item['pr_name'],
                                         'amount': 1}
    session['basket'] = bask



@blueprint_order.route('/save_order', methods=['GET', 'POST'])
@login_required
def save_order():
    order_id = None
    user_id = session.get('user_id')
    dbconfig = current_app.config['dbconfig']

    # Проверка наличия ключа 'basket' в объекте session
    if 'basket' in session and session['basket']:
        with DBContextManager(dbconfig) as cursor:
            if cursor:
                sql = provider.get('insert_order.sql', user_id=user_id, user_date=datetime.now().strftime("%Y-%m-%d"))
                cursor.execute(sql)
                order_id = cursor.lastrowid
                print("1")
                print(order_id)
                if order_id:
                    for key in session['basket'].keys():
                        item = session['basket'][key]
                        sql = provider.get('insert_order_list.sql', order_id=order_id, id_product=key,
                                           product_amount=item['amount'])
                        print(sql)
                        cursor.execute(sql)
                else:
                    return redirect(url_for('bp_order.choose'))

    else:
        return redirect(url_for('bp_order.choose'))

    if not session['basket']:
        session['basket'] = {}  # Устанавливаем корзину, если ее не было

    session['basket'] = {}  # Очищаем корзину после оформления заказа
    return render_template('done.html')



@blueprint_order.route('/sec')
@login_required
@group_required
def menu():
    session.pop('basket', None)
    return redirect(url_for('menu_choice'))


@blueprint_order.route('/clear')
@login_required
@group_required
def clear_basket():
    session['basket'] = {}
    return redirect(url_for('bp_order.choose'))
















