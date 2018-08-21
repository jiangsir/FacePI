import pymysql.cursors
import ClassUtils
import traceback
import re
from urllib.parse import urlparse

#cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D INSTALL_PYTHON_EXAMPLES=ON -D INSTALL_C_EXAMPLES=ON -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules -D BUILD_EXAMPLES=ON ..

class BaseDB(object):
    @classmethod
    def __connect(self):
        config = ClassUtils.loadConfig()
        conn = pymysql.connect(
            host=config['dbhost'],
            port=int(config['dbport']),
            user=config['dbuser'],
            password=config['dbpass'],
            db='facepi',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor)
        return conn

    @classmethod
    def create_conn(self):
        try:
            ''' 連接 mysql '''
            conn = self.__connect()
            return conn
        except pymysql.err.OperationalError as e:
            print('捕獲資料庫錯誤: 無法連線資料庫', e)
            traceback.print_tb(e.__traceback__)
            return None
        except pymysql.err.InternalError as e:
            if e.args[1].startswith('Unknown database'):
                print('資料庫不存在, 請自行創建資料庫')
            else:
                print('捕獲資料庫錯誤:', e)
                print('args[1] = ', e.args[1])
            traceback.print_tb(e.__traceback__)
            return None
        except BaseException as e:
            print('已捕獲的 BaseException:', e)
            traceback.print_tb(e.__traceback__)
            return None

    @classmethod
    def create_table(self):
        ''' 當資料表不存在時, 創建整個資料資料表 '''
        conn = self.create_conn()
        try:
            cursor = conn.cursor()
            # cursor.execute("CREATE DATABASE IF NOT EXISTS facepi")
            # INSERT INTO signins(personid, name, confidence, info, timestamp, faceimage) 
            sql = '''
            CREATE TABLE IF NOT EXISTS `facepi`.`signins` 
            ( `id` INT NOT NULL AUTO_INCREMENT , 
            `personid` VARCHAR(200) NOT NULL , 
            `name` VARCHAR(200) NOT NULL , 
            `confidence` VARCHAR(200) NOT NULL , 
            `info` VARCHAR(200) NOT NULL , 
            `timestamp` DATETIME NOT NULL , 
            `faceimage` LONGBLOB NOT NULL , 
            PRIMARY KEY (`id`)) ENGINE = InnoDB;
            '''
            cursor.execute(sql)

            # persons(personid, name, userdata)
            sql = '''
            CREATE TABLE IF NOT EXISTS `facepi`.`persons` 
            ( `id` INT NOT NULL AUTO_INCREMENT , 
            `personid` VARCHAR(200) NOT NULL , 
            `name` VARCHAR(200) NOT NULL , 
            `userdata` VARCHAR(200) NOT NULL , 
            PRIMARY KEY (`id`)) ENGINE = InnoDB;
            '''
            cursor.execute(sql)
            conn.commit()
            cursor.close()
        except BaseException as e:
            traceback.print_tb(e.__traceback__)
            return None
        finally:
            conn.close()

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
    def insert(self, personId, name, confidence, info, timestamp, faceimage):
        """
        新增操作
        :param sql:
        :param params:
        :return:
        """

        conn = self.create_conn()
        try:

            sql = '''INSERT INTO signins(personid, name, confidence, info, timestamp, faceimage) 
            VALUES(%s, %s, %s, %s, %s, %s)'''
            params = (personId, name, confidence, info, timestamp, faceimage)
            cursor = conn.cursor()
            result = cursor.execute(sql, params)
            conn.commit()
            cursor.close()
            return result
        except pymysql.err.ProgrammingError as e:
            if re.match("Table (.+) doesn't exist", e.args[1]):
                self.create_table()
                return self.insert(personId, name, confidence, info, timestamp, faceimage)
            traceback.print_exc()
            return None
        except BaseException as e:
            print('已捕獲的 BaseException:', e)
            # traceback.print_tb(e.__traceback__)
            traceback.print_exc()
            return None
        finally:
            if conn != None:
                conn.close()


if __name__ == "__main__":
    sql = 'SELECT * FROM persons'
    BaseDB.execute('INSERT INTO persons(personid, name, userdata) VALUES(%s, %s, %s)',
                   ('personiddddd', 'nameeeee', 'userdataaaaa'))
    res = BaseDB.query(sql, None)
    print(res)
