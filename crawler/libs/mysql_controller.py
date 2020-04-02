import pymysql
import json


class MySQLController:

    def __init__(self):
        with open('config/config.json') as f:
            self.config = json.load(f)

        host = self.config['host']
        user = self.config['user']
        password = self.config['password']
        db = self.config['db']

        self.conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8')
        self.curs = self.conn.cursor()

        print('MySQLController init')

    def __del__(self):
        self.conn.close()

        print('MySQLController del')

    def insert_petition_meta(self, petition_meta):
        sql = "INSERT INTO petition_meta " \
              "(no, category, n_participants, date_expired, date_start, detail_url, title) " \
              "VALUES " \
              "(%s, %s, %s, %s, %s, %s, %s)"

        self.curs.execute(sql, (
            petition_meta.no, petition_meta.category,
            petition_meta.n_participants,
            petition_meta.date_expired, petition_meta.date_start,
            petition_meta.detail_url, petition_meta.title
        ))

        self.conn.commit()

        return self.curs.lastrowid

    def select_all_petition_meta(self):
        sql = "SELECT * FROM petition_meta"
        self.curs.execute(sql)

        rows = self.curs.fetchall()
        print(rows)

    def insert_petition_body(self, petition_body):
        sql = "INSERT INTO petition_body (id, body) VALUES (%s, %s)"
        self.curs.execute(sql, (petition_body.petition_meta_id, petition_body.body))

        self.conn.commit()

        return self.curs.lastrowid

    def select_all_petition_body(self):
        sql = "SELECT * FROM petition_body"
        self.curs.execute(sql)

        rows = self.curs.fetchall()
        print(rows)

    def insert_word(self, words):
        sql = "INSERT INTO word (text, morpheme, petition_meta_id, position) VALUES (%s, %s, %s, %s)"
        self.curs.executemany(sql, words)

        self.conn.commit()

    def select_all_word(self):
        sql = "SELECT * FROM word"
        self.curs.execute(sql)

        rows = self.curs.fetchall()
        print(rows)

    def select_last_petition_id(self):
        sql = "SELECT no FROM petition_meta ORDER BY no DESC"
        self.curs.execute(sql)

        row = self.curs.fetchone()

        return row and row[0] or None
