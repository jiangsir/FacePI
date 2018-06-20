import pymysql.cursors, ClassUtils
from urllib.parse import urlparse

class BaseDB(object):
    @classmethod
    def create_conn(self):
        ''' 連接 mysql '''
        config = ClassUtils.loadConfig()
        return pymysql.connect(
            host=config['dbhost'],
            port=config['dbport'],
            user=config['dbuser'],
            password=config['dbpass'],
            db='facepi',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor)

    @classmethod
    def query(self, sql, params):
        """
        查詢
        :param sql:
        :param params:
        :return:
        """
        conn = self.create_conn()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            result = cursor.fetchall()
            cursor.close()
            return result
        except BaseException as e:
            print(e)
            return []
        finally:
            conn.close()

    @classmethod
    def execute(self, sql, params):
        """
        更新操作
        :param sql:
        :param params:
        :return:
        """
        conn = self.create_conn()
        try:
            cursor = conn.cursor()
            result = cursor.execute(sql, params)
            conn.commit()
            cursor.close()
            return result
        except BaseException as e:
            print(e)
            return False
        finally:
            conn.close()

    @classmethod
    def insert(self, sql, params):
        """
        新增操作
        :param sql:
        :param params:
        :return:
        """
        conn = self.create_conn()
        try:
            cursor = conn.cursor()
            result = cursor.execute(sql, params)
            conn.commit()
            cursor.close()
            return result
        except BaseException as e:
            print(e)
            return False
        finally:
            conn.close()

if __name__ == "__main__":
    sql = 'SELECT * FROM persons'
    BaseDB.execute('INSERT INTO persons(personid, name, userdata) VALUES(%s, %s, %s)', ('personiddddd', 'nameeeee', 'userdataaaaa'))
    res = BaseDB.query(sql, None)
    print(res)
