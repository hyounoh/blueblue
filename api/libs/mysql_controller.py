import pymysql
import json


class MySQLController:

  def __init__(self):
    with open('config/config.json') as f:
      self.config = json.load(f)

    with open('config/stopword.json', encoding='UTF8') as f:
      self.stopwords = json.load(f)

    self.host = self.config['host']
    self.user = self.config['user']
    self.password = self.config['password']
    self.db = self.config['db']

    print('MySQLController init')

  def __del__(self):
    print('MySQLController del')

  def wordcloud(self, use_stopword=1, limit=10):

    conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, charset='utf8')
    curs = conn.cursor()

    # Compose where clause if using stopword
    where_clause = None
    if use_stopword:
      where_clause = "WHERE "
      for stopword in self.stopwords['stopword']:
        where_clause += 'NOT `text` = ' + '\"' + stopword + '\" AND '
      where_clause = where_clause[:len(where_clause) - 4]

    sql = ""
    sql += "SELECT text, COUNT(*) as count FROM word "
    sql += where_clause if where_clause else ""
    sql += "GROUP BY `text` ORDER BY count DESC "
    sql += "LIMIT " + str(limit) + ";"

    curs.execute(sql)

    rows = curs.fetchall()

    conn.close()

    return rows

  def recentword(self, use_stopword=1):

    conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, charset='utf8')
    curs = conn.cursor()

    # Compose where clause if using stopword
    where_clause = "WHERE w.petition_meta_id = pm.id AND pm.date_start > DATE(NOW()) - INTERVAL 7 DAY "
    if use_stopword:
      for stopword in self.stopwords['stopword']:
        where_clause += 'AND NOT `text` = ' + '\"' + stopword + '\" '

    sql = ""
    sql += "SELECT text, COUNT(*) as count FROM word w, petition_meta pm "
    sql += where_clause if where_clause else ""
    sql += "GROUP BY `text` ORDER BY count DESC "
    sql += "LIMIT 3;"

    curs.execute(sql)

    rows = curs.fetchall()

    conn.close()

    return rows

  def petition_graph(self, recent=True):

    conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, charset='utf8')
    curs = conn.cursor()

    sql = "SELECT DATE_FORMAT(pm.date_start, '%Y-%m-%d') as date, COUNT(*) as count FROM petition_meta pm"
    sql += " WHERE pm.date_start > DATE(NOW()) - INTERVAL 7 DAY" if recent else ""
    sql += " GROUP BY pm.date_start ORDER BY pm.date_start DESC"
    sql += ";" if recent else " LIMIT 30;"

    curs.execute(sql)

    rows = curs.fetchall()

    conn.close()

    return rows

  def petition_word(self, keyword):

    conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, charset='utf8')
    curs = conn.cursor()

    sql = "SELECT DISTINCT w.`text`, pm.title, pm.detail_url, pm.date_start, pm.no "
    sql += "FROM word w, petition_meta pm "
    sql += "WHERE w.`text` = \"" + keyword + "\" AND w.petition_meta_id = pm.id "
    sql += "ORDER BY pm.date_start DESC, pm.no DESC "
    sql += "LIMIT 25;"

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
