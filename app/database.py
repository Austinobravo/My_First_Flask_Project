import mysql.connector
import sqlite3

conn = mysql.connector.connect(host="localhost", user="root",password="password", database="blockchain")
cursor = conn.cursor(dictionary=True)


def database(data):
    sql = "select * from coins where coinname like % {} % ".format(data)
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows

def single_database(id):
    sql = "SELECT * FROM coins WHERE id={}".format(id)
    cursor.execute(sql)
   
    rows = cursor.fetchall()
    for row in rows:
        row
    if not rows:
        return None

    return row
def blog():
    sql = "SELECT * FROM blog"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows
def blogdetailsdatabase(data):
    sql = "INSERT INTO blog (title,blogdetails, image) VALUES (%s,%s,LOAD_FILE('%s'))"
    datas = (data['name'], data['blogdetails'], data['image'])
    cursor.execute(sql, datas)
def sqlitedatabase(data):
    conns= sqlite3.connect("mydb.db")
    cursors = conns.cursor()
    cursors.execute("""Drop table blog""")
    cursors.execute("""create table if not exists blog(title text, data mediumblop)""")
    cursors.execute(""" insert into blog (title, data) values (?,?)""", ('name', data))
    conns.commit()
    cursors.close()
    conns.close() 

    print('Data inserted')
def contact_form(data):
    sql = "INSERT INTO contact_form (full_name, email, phone, message) VALUES (%s,%s,%s,%s)"
    # datas = (data['name'],data['email'],data['phone_no'], data['message'])
    datas = ('name', 'email', '3', 'i am here')
    try:
        cursor.execute(sql, datas)
        print("Data inserted")
    except:
        # conn.rollback()
        print("data not inserted")
    




from sqlalchemy import create_engine, text
# print(sqlalchemy.__version__)
conn = mysql.connector.connect(host="localhost", user="root",password="password", database="blockchain")
cursor = conn.cursor(dictionary=True)
sql = "select * from coins"
curor =cursor.execute(sql)
print(curor)
rows = cursor.fetchall()
print('r',rows[0])
# col = []
# for en in rows:
#     col.append(en)
#     print(col)

engine = create_engine("mysql+pymysql://root:password@localhost/blockchain?charset=utf8mb4")
# with engine.connect() as conn:
#     result = conn.execute (text("select * from coins"))
    # print(iter(result.all()))
    # print(type(result.all()))
    # result_all = result.all()
    # dicts= dict(result_all[0])
    # print(result)
    # resuly_all  = list(result)
    # print('list', resuly_all)
    # result_all = dict(list(result))
    # print('dict:', result_all)
    # db_list = []
    # for list in result.all():
    #     db_list.append(dict(list))

    #     # db_list[result_all[list]] = result_all[list + 1]
    # # return db_list
    #     print(db_list )
    