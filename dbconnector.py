import dbconfig
import mysql.connector as _connector
from mysql.connector import errorcode as dberror

class Connector:
	def __init__(self):
		self.cnx = self.cur = None
		try:
			self.cnx = _connector.connect(**dbconfig.config)
		except _connector.Error as e:
			if(e.errno  == dberror.ER_ACCESS_DENIED_ERROR):
				print('Invalid credentials')
			elif(e.errno == dberror.ER_BAD_DB_ERROR):
				print('Invalid database')
			else:
				print(e)
		else:
			self.cur = self.cnx.cursor()

	def test_select(self):
		self.cur.execute("SELECT * FROM users AS U LIMIT 10")
		print()
		print('{0:3} {1:25} {2}'.format('ID:', 'EMAIL:', 'LANG:'))
		for row in self.cur.fetchall():
			print('{0:3} {1:25} {2}'.format(row[0], row[2], row[4]))
		print()

	def insert_ignore(self, table, data_dictionary):
		insert_id = None
		keys = "("+", ".join( "`"+key+"`" for key in data_dictionary.keys() )+")"
		values = "("+", ".join( "%("+str(value)+")s" for value in data_dictionary.keys() )+")"
		query = ("INSERT IGNORE INTO {0}\n"
			"{1}\n"
			"VALUES {2}".format(table, keys, values) )
		try:
			self.cur.execute(query, data_dictionary)
			self.cnx.commit()
			insert_id = self.cur.lastrowid
		except Exception as e:
			print(e)
		return insert_id

	def main(self):
		id = self.insert_ignore('analytics_hostname_stats', {
			'hostname': 'hostname',
			'sessions': 1,
			'page_views': 1,
			'avg_time_on_page': 2.1,
			'exits': 3,
			'organic_searches': 5,
			'date': '2017-07-31',
		})
		print(id)
		if self.cur:
			self.cur.close()
		if self.cnx:
			self.cnx.close()


if __name__ == '__main__':
	connector = Connector()
	connector.main()