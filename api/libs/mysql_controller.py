import pymysql
import json


class MySQLController:

  def __init__(self):
    with open('config/config.json') as f:
      self.config = json.load(f)

    self.host = self.config['host']
    self.user = self.config['user']
    self.password = self.config['password']
    self.db = self.config['db']

    self.stopwords = self.read_stopword()

    print('MySQLController init')

  def __del__(self):
    print('MySQLController del')

  def read_words(self, use_stopword, limit, interval):
    conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, charset='utf8')
    curs = conn.cursor()

    # Compose where clause if using stopword
    where_clause = "WHERE w.petition_meta_id = pm.id AND pm.date_start > DATE(NOW()) - INTERVAL " + str(interval) + " DAY "
    if use_stopword:
      for stopword in self.stopwords:
        where_clause += 'AND NOT `text` = ' + '\"' + stopword[1] + '\" '

    sql = ""
    sql += "SELECT text, COUNT(*) as count FROM word w, petition_meta pm "
    sql += where_clause
    sql += "GROUP BY `text` ORDER BY count DESC "
    sql += "LIMIT " + str(limit) + ";"

    curs.execute(sql)
    rows = curs.fetchall()
    conn.close()

    return rows

  def read_graph(self, interval):

    conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, charset='utf8')
    curs = conn.cursor()

    sql = "SELECT DATE_FORMAT(pm.date_start, '%Y-%m-%d') as date, COUNT(*) as count FROM petition_meta pm "
    sql += "WHERE pm.date_start > DATE(NOW()) - INTERVAL " + str(interval) + " DAY "
    sql += "GROUP BY pm.date_start ORDER BY pm.date_start DESC;"

    curs.execute(sql)
    rows = curs.fetchall()
    conn.close()

    return rows

  def read_petitions(self, keyword, interval):

    conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, charset='utf8')
    curs = conn.cursor()

    sql = "SELECT DISTINCT w.`text`, pm.title, pm.detail_url, pm.date_start, pm.no "
    sql += "FROM word w, petition_meta pm "
    sql += "WHERE pm.date_start > DATE(NOW()) - INTERVAL " + str(interval) + " DAY AND w.`text` = \"" + keyword + "\" AND w.petition_meta_id = pm.id "
    sql += "ORDER BY pm.date_start DESC, pm.no DESC;"

    curs.execute(sql)
    rows = curs.fetchall()
    conn.close()

    return rows

  def create_stopword(self, stopword):

    conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, charset='utf8')
    curs = conn.cursor()

    sql = "INSERT INTO stopword (word) VALUES (%s)"

    curs.execute(sql, stopword)
    conn.commit()
    conn.close()

    return curs.lastrowid

  def read_stopword(self):

    conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, charset='utf8')
    curs = conn.cursor()

    sql = "SELECT * FROM stopword;"

    curs.execute(sql)
    rows = curs.fetchall()
    conn.close()

    return rows
