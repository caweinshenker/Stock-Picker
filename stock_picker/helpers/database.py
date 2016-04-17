import psycopg2
import psycopg2.extras
import getpass

class Db():

	def __init__(self):
		self.conn = self.__init_db()
		self.cur = self.__connect_db(self.conn)
			
	def __init_db(self): 
		 try:  
		 	connectionString = 'dbname = caweinsh_sp3 user=caweinsh password=f6nt0d host=localhost'
			conn = psycopg2.connect(connectionString)
		 except Exception as e: 
			 print(str(e))
		 return conn

	def __connect_db(self, conn):
		return conn.cursor()

	def __close_db(self, cur, conn):
		conn.commit()
		cur.close()
		conn.close()

	def get_cur(self):
		return self.cur

	def get_conn(self):
		return self.conn

	def execute(self, SQL, data):
		self.cur.execute(SQL, data)
