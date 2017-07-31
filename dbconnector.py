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

	def main(self):
		self.test_select()


if __name__ == '__main__':
	connector = Connector()
	connector.main()