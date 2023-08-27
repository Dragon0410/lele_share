# /usr/bin python3
# -*- encoding:utf-8 -*-
# create date: 2023/8/27
# create time: 16:35
# create author: 93207
# describe:
import traceback

import pymssql

from utils.loguru_logging import Logger




class ServerSQLHandler(Logger):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kwargs = kwargs
        self.conn = None
        self.cursor = None

    def _connect(self):
        """
        :create author: 93207
        :create time: 2023/8/27 19:10
        """
        conn_status = True
        try:
            self.conn = pymssql.connect(**self.kwargs)
            self.cursor = self.conn.cursor(as_dict=True)
        except Exception as e:
            self.log.error(traceback.format_exc())
            conn_status = False
        finally:
            return conn_status

    def _close(self):
        """
        :create author: 93207
        :create time: 2023/8/27 19:12
        """
        if self.cursor:
            self.cursor.close()

        if self.conn:
            self.conn.close()

    def __enter__(self):
        """
        :create author: 93207
        :create time: 2023/8/27 19:13
        """
        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        :create author: 93207
        :create time: 2023/8/27 19:14
        """
        if all([exc_type, exc_val, exc_tb]):
            self.log.error(traceback.format_exc())
        self._close()

    def get_one_data(self, sql_text) -> list:
        """
        :create author: 93207
        :create time: 2023/8/27 19:15
        """
        results = []
        try:
            self.cursor.execute(sql_text)
            results = self.cursor.fetchone()
        except Exception as e:
            self.log.error(traceback.format_exc())
        finally:
            return results

    def get_many_data(self, sql_text, many_number: int = 10000) -> list:
        """
        :create author: 93207
        :create time: 2023/8/27 19:16
        """
        results = []
        try:
            self.cursor.execute(sql_text)
            results = self.cursor.fetchmany(many_number)
        except Exception as e:
            self.log.error(traceback.format_exc())
        finally:
            return results

    def get_all_data(self, sql_text) -> list:
        """
        :create author: 93207
        :create time: 2023/8/27 19:17
        """
        results = []
        try:
            self.cursor.execute(sql_text)
            results = self.cursor.fetchall()
        except Exception as e:
            self.log.error(traceback.format_exc())
        finally:
            return results

    def create_table(self, sql_text):
        """
        :create author: 93207
        :create time: 2023/8/27 19:18
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
        :create time: 2023/8/27 19:19
        """
        create_status = True
        try:
            self.cursor.execute(sql_text)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            self.log.error(traceback.format_exc())
            create_status = False
        finally:
            return create_status

    def insert_one_data(self, sql_text):
        """
        :create author: 93207
        :create time: 2023/8/27 19:20
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

    def insert_many_data(self, sql_text, params):
        """
        :create author: 93207
        :create time: 2023/8/27 19:21
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
