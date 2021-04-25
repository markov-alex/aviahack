import psycopg2
import datetime
from smsc_api import *
from psycopg2.extras import DictCursor

smsc = SMSC()



VERSION = '1.0'

DB_INFO = {'dbname': 'postgres',
           'user': 'postgres',
           'password': '1',
           'host': 'localhost'
           }


def print_human(number):
    conn = psycopg2.connect(dbname=DB_INFO['dbname'], user=DB_INFO['user'], password=DB_INFO['password'],
                            host=DB_INFO['host'])
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(f"""SELECT * FROM human WHERE human.number = '{number}'""")
    print((*cursor))
    conn.close()


def get_docs_human(number):
    conn = psycopg2.connect(dbname=DB_INFO['dbname'], user=DB_INFO['user'], password=DB_INFO['password'],
                            host=DB_INFO['host'])
    cursor = conn.cursor()
    cursor.execute(f"""SELECT document.type, document.content FROM document
                       INNER JOIN signature ON signature.id_document = document.id_document
                       INNER JOIN human ON human.id_human = signature.id_human
                       WHERE human.number = '{number}'""")
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res


def get_menu_doc():
    conn = psycopg2.connect(dbname=DB_INFO['dbname'], user=DB_INFO['user'], password=DB_INFO['password'],
                            host=DB_INFO['host'])
    cursor = conn.cursor()
    cursor.execute('SELECT id_document, type FROM document')
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res


def get_full_doc(id):
    conn = psycopg2.connect(dbname=DB_INFO['dbname'], user=DB_INFO['user'], password=DB_INFO['password'],
                            host=DB_INFO['host'])
    cursor = conn.cursor()
    cursor.execute(f'SELECT content FROM document WHERE id_document = {id}')
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res


def sign(number, id_doc):
    conn = psycopg2.connect(dbname=DB_INFO['dbname'], user=DB_INFO['user'], password=DB_INFO['password'],
                            host=DB_INFO['host'])
    cursor = conn.cursor()
    cursor.execute(f'SELECT id_human FROM human WHERE number = \'{number}\'')
    id_hum = cursor.fetchall()[0][0]
    cur_date = str(datetime.today().date())
    cursor.execute(f"""INSERT INTO signature(date_signing, version, id_human, id_document)
VALUES ('{cur_date}', '{VERSION}', {id_hum}, {id_doc})""")
    conn.commit()
    cursor.close()
    conn.close()
    return 0


def man_in_table(number):
    conn = psycopg2.connect(dbname=DB_INFO['dbname'], user=DB_INFO['user'], password=DB_INFO['password'],
                            host=DB_INFO['host'])
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM human WHERE number = \'{number}\'")
    tmp = len(cursor.fetchall())
    cursor.close()
    conn.close()
    if tmp != 0:
        return True
    else:
        return False

# дата должна быть такой строкой '2021-04-25'
def insert_human_table(name, last_name, second_name, birth_date, number):
    conn = psycopg2.connect(dbname=DB_INFO['dbname'], user=DB_INFO['user'], password=DB_INFO['password'],
                            host=DB_INFO['host'])
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO human(name, last_name, second_name, birth_date, number)
VALUES ('{name}', '{last_name}', '{second_name}', '{birth_date}', '{number}')""")
    conn.commit()
    cursor.close()
    conn.close()


#get_docs_human('89005553512')
#print(get_menu_doc())
#print(get_full_doc(1))
# sign('89634972345', 2)
#print(man_in_table('89005553512'))
#smsc.send_sms("+7933333333", "Ася, это Мага пишет с пайтона, УРА!\n Как у тебя дела? Напиши мне вк, если прочтешь)", sender="magomed")

