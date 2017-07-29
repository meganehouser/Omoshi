import sqlite3
from app import app


def execute_sql(db, sql):
    print(sql)
    with sqlite3.connect(db,
            detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES) as con:

        cur = con.cursor()
        cur.executescript(sql)
        con.commit()

if __name__ == '__main__':
    with open('schema.sql', encoding='utf-8') as f:
        execute_sql(app.config['DATABASE'], f.read())
