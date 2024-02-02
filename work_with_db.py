from DBcm import DBContextManager
from typing import Tuple, List


def select_dict(db_config: dict, _sql: str):
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        else:
            cursor.execute(_sql)
            rk6 = cursor.fetchall()
            if rk6:
                procurements_dict = []
                schema = [item[0] for item in cursor.description]
                for procurement in rk6:
                    procurements_dict.append(dict(zip(schema, procurement)))
                return procurements_dict
            else:
                return None

def call_proc(dbconfig: dict, proc_name: str, *args):
    with DBContextManager(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        param_list = []
        for arg in args:
            param_list.append(arg)
        res = cursor.callproc(proc_name, param_list)
        return res



#новое
def insert(db_config:dict, _sql: str):
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Cursor not found')
        result = cursor.execute(_sql)
    return result

def update(db_config:dict, _sql:str):
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Update cursor not found')
        result = cursor.execute(_sql)
    return result

def select(db_config: dict, sql: str) -> Tuple[Tuple, List[str]]:
    result = tuple()
    schema = []
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Cursor not found')
        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        result = cursor.fetchall()
    return result, schema