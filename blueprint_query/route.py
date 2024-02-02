import os
import logging
from flask import Blueprint, render_template, request, current_app, session
from work_with_db import select_dict
from sql_provider import SQLProvider


from authentication_blueprint.access import group_required
logging.basicConfig(level=logging.DEBUG)

blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/query_menu', methods = ['GET', 'POST'])
def start_index():
    return render_template("main_menu.html")


@blueprint_query.route('/query1', methods=['GET', 'POST'])
@group_required
def query_index1():
    if request.method == 'POST':
        # _sql = provider.get('shipper1.sql')
        _sql = "SELECT a.sh_id, a.sh_name FROM rk6.shipper a LEFT JOIN rk6.invoice b ON a.sh_id = b.sh_id WHERE in_id IS NULL;"
        logging.debug(f"Executing SQL query: {_sql}")

        print(_sql)
        shippers = select_dict(current_app.config['dbconfig'], _sql)
        logging.debug(f"Shippers data: {shippers}")

        print(shippers)
        if shippers:
            prod_title = 'Результат'
            return render_template('dynamic_sh.html', prod_title=prod_title, shippers=shippers)
        else:
            return render_template('error.html')
    # _sql = provider.get('shipper1.sql')
    _sql = "SELECT a.sh_id, a.sh_name FROM rk6.shipper a LEFT JOIN rk6.invoice b ON a.sh_id = b.sh_id WHERE in_id IS NULL;"
    shippers = select_dict(current_app.config['dbconfig'], _sql)
    prod_title = 'Результат'
    return render_template('dynamic_sh.html', prod_title=prod_title, shippers=shippers)



@blueprint_query.route('/query')
@group_required
def query_index():
    return render_template('queries.html')



@blueprint_query.route('/querypr1', methods=['GET', 'POST'])
@group_required
def query_index_pr1():
    if request.method == 'POST':
        # _sql = "select	* from rk6.procurement a join rk6.store b on a.pr_id = b.prr_id where st_price = (select max(st_price) from rk6.store);"
        _sql = "select	* from rk6.procurement a join rk6.store b on a.pr_id = b.prr_id where st_price = (select max(st_price) from rk6.store);"
        procurements = select_dict(current_app.config['dbconfig'], _sql)
        # logging.basicConfig(filename='app.log', level=logging.DEBUG)
        # logging.debug(shippers)
        if procurements:
            prod_title = 'Результат'
            print("Data from procurements_dict:")
            print(procurements)
            return render_template('dynamic_pr_all.html', prod_title=prod_title, procurements=procurements)
        else:
            return render_template('error.html')

    _sql = "select	* from rk6.procurement a join rk6.store b on a.pr_id = b.prr_id where st_price = (select max(st_price) from rk6.store);"
    procurements = select_dict(current_app.config['dbconfig'], _sql)
    prod_title = 'Результат'
    return render_template('dynamic_pr_all.html', prod_title=prod_title, procurements=procurements)


@blueprint_query.route('/querypr2', methods=['GET', 'POST'])
@group_required
def query_index_pr2():
    if request.method == 'POST':
        pr_year = request.form.get('pr_year')
        # print(f"Year received from form: {pr_year}")
        # _sql = provider.get('procurement2.sql', pr_year=pr_year)
        _sql = f"select month(in_date), pr_id, sum(il_quantity) from rk6.invoice a  join rk6.invoice_line b on a.in_id = b.in_id where year(in_date) = {pr_year} group by month(in_date), pr_id;"

        shippers = select_dict(current_app.config['dbconfig'], _sql)
        print("Data from procurements_dict:")
        print(shippers)
        logging.basicConfig(filename='app.log', level=logging.DEBUG)
        logging.debug(shippers)
        logging.info(f"SQL query to execute: {_sql}")

        if shippers:
            prod_title = 'Вот результат из БД'
            # print("Data from procurements_dict:")
            # print(shippers)
            return render_template('dynamic_pr.html', prod_title=prod_title, shippers=shippers)
        else:
            return render_template('error.html')
    return render_template('input_procurement2.html')




