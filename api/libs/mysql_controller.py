import pymysql
import json


class MySQLController:

    def __init__(self):
        with open('config/config.json') as f:
            self.config = json.load(f)

        with open('config/stopword.json', encoding='UTF8') as f:
            self.stopwords = json.load(f)

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

    def wordcloud(self, use_stopword=1, limit=10):

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

        self.curs.execute(sql)

        rows = self.curs.fetchall()

        return rows

    def petition_graph(self, recent=True):

        sql = "SELECT DATE_FORMAT(pm.date_start, '%Y-%m-%d') as date, COUNT(*) as count FROM petition_meta pm"
        sql += " WHERE pm.date_start > DATE(NOW()) - INTERVAL 7 DAY" if recent else ""
        sql += " GROUP BY pm.date_start ORDER BY pm.date_start DESC"
        sql += ";" if recent else " LIMIT 30;"

        self.curs.execute(sql)

        rows = self.curs.fetchall()

        return rows

    def petition_word(self, keyword):

        sql = "SELECT DISTINCT w.`text`, pm.title, pm.detail_url, pm.date_start, pm.no "
        sql += "FROM word w, petition_meta pm "
        sql += "WHERE w.`text` = \"" + keyword + "\" AND w.petition_meta_id = pm.id "
        sql += "ORDER BY pm.date_start DESC, pm.no DESC "
        sql += "LIMIT 25;"

        self.curs.execute(sql)

        rows = self.curs.fetchall()

        return rows
