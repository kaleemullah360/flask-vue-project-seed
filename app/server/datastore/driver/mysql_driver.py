
# MySQL Database Driver

import MySQLdb as mdb
from utils.print import ppp

import time


class MySqlDriver():
	"""
	MySQL database driver which implements CRUD and utility public methods.
	"""


	RECORD_CREATED_TS_COLUMN = 'created_ts'
	RECORD_UPDATED_TS_COLUMN = 'updated_ts'


	def __init__(self, database_name):
		self.database_name = self.__escape(database_name)
		self.conn = mdb.connect(
			host='mysql', # replace with config val
			user='root', # replace with config val
			passwd='password', # replace with config val
			db=database_name
		)
		self.cur = self.conn.cursor(mdb.cursors.DictCursor)
		self.conn.set_character_set('utf8')
		self.cur.execute('SET NAMES utf8;')
		self.cur.execute('SET CHARACTER SET utf8;')
		self.cur.execute('SET character_set_connection=utf8;')


	########## CRUD INTERFACE METHODS ##########

	def insert(self, table_name, value_props={}):
		"""
		MySQL driver interface method for single record inserts.

		Args:
			table_name (str): Name of MySQL table.
			value_props (dict): Dictionary of column insert values where
				key=column name and value=column value.

		Returns:
			id of the inserted record

		"""

		value_props[self.RECORD_CREATED_TS_COLUMN] = int(time.time())
		value_props[self.RECORD_UPDATED_TS_COLUMN] = int(time.time())

		fields = []
		values = []
		for key, val in value_props.items():
			fields.append(key)
			values.append(val)

		fields_str = ', '.join([
			"`{}`".format(self.__escape(field))
			for field in fields
		])
		values_str_sub = ', '.join(['%s' for item in values])

		query_stmt = """
			INSERT INTO `{0}` ({1})
			VALUES ({2});
		""".format(
			self.__escape(table_name),
			fields_str,
			values_str_sub
		)

		with self.conn:
			self.cur.execute(query_stmt, tuple(values))
			return self.cur.lastrowid


	def find_by_fields(self, table_name, where_props={}, limit=None):
		"""
		MySQL driver interface method for finding records by conditionals.

		Args:
			table_name (str): Name of MySQL table.
			where_props (dict): Dictionary of 'where' clause values where
				key=column name and value=column value.
			limit (int or None): Positive integer limit for query results list.

		Returns:
			List of dictionaries representing MySQL records (deserialized)

		"""

		query_stmt_components = []

		select_component = 'SELECT * FROM `{}`'.format(
			self.__escape(table_name)
		)
		query_stmt_components.append(select_component)

		where_values = None
		if len(where_props.keys()) > 0:
			where_component = 'WHERE ' + ' AND '.join([
				'`{}`=%s'.format(self.__escape(key))
				for key, val in where_props.items()
			])
			query_stmt_components.append(where_component)
			where_values = tuple([
				val for key, val in where_props.items()
			])

		if(limit is not None and int(limit) > 0):
			limit_component = 'LIMIT {}'.format(self.__escape(str(limit)))
			query_stmt_components.append(limit_component)

		query_stmt = ' '.join(query_stmt_components) + ';'

		with self.conn:
			if where_values is not None:
				self.cur.execute(query_stmt, where_values)
			else:
				self.cur.execute(query_stmt)
			return self.cur.fetchall()


	def update_by_fields(self, table_name, value_props={}, where_props={}):
		ppp('MySqlDriver.update_by_fields not implemented yet...')
		print(self.cur._last_executed)
		# ex:
		# UPDATE table_name SET field1 = new-value1, field2 = new-value2
		# [WHERE Clause]
		pass

	def delete_by_fields(self, table_name, where_props={}):
		ppp('MySqlDriver.delete_by_fields not implemented yet...')
		# ex:
		# DELETE FROM table_name [WHERE Clause]
		pass


	########## DATABASE UTILITIES ##########

	def create_table(self, table_name, column_props={}):
		ppp('MySqlDriver.create_table not implemented yet...')
		# CREATE TABLE example(
		# 	id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
		# 	example_column VARCHAR(255)
		# );
		pass

	def delete_table_contents(self, table_name):
		ppp('MySqlDriver.delete_table_contents not implemented yet...')
		# TRUNCATE TABLE table_name;
		pass

	def delete_table(self, table_name):
		ppp('MySqlDriver.delete_table not implemented yet...')
		# DROP TABLE table_name
		pass

	def get_database_size(self):
		query_stmt = """
			SELECT table_name AS "Table",
			ROUND(((data_length + index_length) / 1024 / 1024), 2)
			AS "Size (MB)"
			FROM information_schema.TABLES
			WHERE table_schema = "{}"
			ORDER BY (data_length + index_length) DESC;
		""".format(self.database_name)
		with self.conn:
			self.cur.execute(query_stmt)
		return self.cur.fetchall()

	def describe_table(self, table_name):
		query_stmt = "DESC {};".format(
			self.__escape(table_name)
		)
		with self.conn:
			self.cur.execute(query_stmt)
		return self.cur.fetchall()


	########## PRIVATE HELPERS ##########

	# escape strings for use in query strings
	def __escape(self, string):
		return mdb.escape_string(string).decode('utf-8')


