#!/usr/bin/python3

import logging
import time

import pymysql

from helpers.functions import close

class DBManager:
    def __init__(self, config):
        self.logger = logging.getLogger('crawler.DBManager')
        self.host = config['host']
        self.username = config['username']
        self.password = config['password']
        self.database = config['database']
        self.connection = self.cursor = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host = self.host,
                user = self.username,
                passwd = self.password,
                db = self.database,
                use_unicode = True,
                charset = 'utf8'
            )
            self.cursor = self.connection.cursor()
            self.logger.info('Database -> Connected')

        except pymysql.err.OperationalError as error:
            self.logger.error(error)
            close()

    def insert(self, data):
        table = data['type'] + 's'
        if not self.cursor.execute('SELECT (1) from {} where url = %s limit 1'.format(table), data['data']['url']):
            keys = list(data['data'].keys())
            values = list(data['data'].values())
            values += 2 * [time.strftime('%Y-%m-%d %H:%M:%S')]
            sql = 'INSERT INTO {0} ({1}, created_at, updated_at) VALUES ({2})'.format(table, ', '.join(keys), str(values)[1:-1])
            self.cursor.execute(sql)
            self.connection.commit()
            self.logger.info('Database -> {} added'.format(data['type'].capitalize()))
        else:
            self.logger.info('Database -> {} already in database'.format(data['type'].capitalize()))

    def close(self):
        self.cursor.close()
        self.connection.close()
        self.logger.info('Database -> Connection closed')
