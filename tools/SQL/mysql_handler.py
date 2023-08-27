# /usr/bin python3
# -*- encoding:utf-8 -*-
# create date: 2023/8/27
# create time: 16:34
# create author: 93207
# describe:
import traceback

import pymysql

from utils.loguru_logging import Logger




class MySQLHandler(Logger):
    """
    pymysql 对MySQL数据库的操作
    """

    def __init__(self, host: str = None, user: str = None, password: str = None, database: str = None, port: int = 3306,
            charset: str = 'utf-8', connect_timeout: int = 60, autocommit: bool = True, db: str = None,
            passwd: str = None, **kwargs):
        super().__init__(**kwargs)

        if not all([host, user, database]):
            self.server_info.update(kwargs)
        else:
            self.server_info = {
                'host': host,
                'port': port,
                'user': user,
                'password': password,
                'passwd': passwd,
                'database': database,
                'db': db,
                'charset': charset,
                'connect_timeout': connect_timeout,
                'autocommit': autocommit,
            }

        self.conn = None
        self.cursor = None

    def _connect(self):
        """
        :create author: 93207
        :create time: 2023/8/27 16:37
        """
        conn_status = True
        try:
            self.conn = pymysql.connect(**self.server_info)
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        except Exception as e:
            error_msg = f"链接数据库失败。{e}"
            self.log.error(traceback.format_exc())
            conn_status = False
        finally:
            return conn_status

    def _close(self):
        """
        :create author: 93207
        :create time: 2023/8/27 16:53
        """
        if self.cursor:
            self.cursor.close()

        if self.conn:
            self.conn.close()

    def __enter__(self):
        """
        :create author: 93207
        :create time: 2023/8/27 16:53
        """
        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        :create author: 93207
        :create time: 2023/8/27 16:54
        """
        if all([exc_type, exc_val, exc_tb]):
            self.log.error(exc_val)
        self._close()

    def get_one_data(self, sql_text) -> list:
        """
        :create author: 93207
        :create time: 2023/8/27 16:59
        """
        results = []
        try:
            self.cursor.execute(sql_text)
            results = self.cursor.fetchone()
        except Exception as e:
            self.log.error(traceback.format_exc())
        return results

    def get_many_data(self, sql_text, many_number=10000) -> list:
        """
        :create author: 93207
        :create time: 2023/8/27 17:01
        """
        results = []
        try:
            self.cursor.execute(sql_text)
            results = self.cursor.fetchmany(many_number)
        except Exception as e:
            self.log.error(traceback.format_exc())
        return results

    def get_all_data(self, sql_text) -> list:
        """
        :create author: 93207
        :create time: 2023/8/27 17:02
        """
        results = []
        try:
            self.cursor.execute(sql_text)
            results = self.cursor.fetchall()
        except Exception as e:
            self.log.error(traceback.format_exc())
        return results

    def __create(self, sql_text) -> bool:
        """
        :create author: 93207
        :create time: 2023/8/27 17:04
        """
        create_status = True
        try:
            self.cursor.execute(sql_text)
        except Exception as e:
            self.log.error(traceback.format_exc())
            create_status = False
        finally:
            return create_status

    def update_table(self, sql_text):
        """
        :create author: 93207
        :create time: 2023/8/27 17:05
        """
        update_status = True
        try:
            self.cursor.execute(sql_text)
            self.conn.commit()
        except Exception as e:
            self.log.error(traceback.format_exc())
            update_status = False
        finally:
            return update_status

    def insert_one_data(self, sql_text):
        """
        :create author: 93207
        :create time: 2023/8/27 17:07
        """
        insert_status = True
        try:
            self.cursor.execute(sql_text)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            self.log.error(traceback.format_exc())
            insert_status = False
        finally:
            return insert_status

    def insert_many_data(self, sql_text, params: list):
        """
        :create author: 93207
        :create time: 2023/8/27 17:08
        """
        insert_status = True
        try:
            self.cursor.executemany(sql_text, params)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            self.log.error(traceback.format_exc())
            insert_status = False
        finally:
            return insert_status
