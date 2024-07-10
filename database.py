import psycopg2
import dbSecret

class Database:
	def __init__(self):
		self.conn = self.connect()
		self.cur = self.conn.cursor()

	def __del__(self):
		if hasattr(self, "cur"):
			self.cur.close()
		if hasattr(self, "conn"):
			self.conn.close()

	def connect(self):
		conn = psycopg2.connect(
			user = dbSecret.dbusername, 
			password = dbSecret.dbpassword,
			host = dbSecret.dbhost,
			port = dbSecret.dbport,
			dbname = dbSecret.dbname,
		    keepalives=1,
    		keepalives_idle=30,
    		keepalives_interval=10,
    		keepalives_count=5
		)
		return conn

	def createTables(self):
		self.cur.execute("""
			CREATE TABLE linkUsage (
				id serial PRIMARY KEY,
				timestamp TIMESTAMPTZ,
				next TEXT,
				msg TEXT
			)
		""")
	
		self.conn.commit()

	def getData(self, offset = 0, count = 5):
		self.cur.execute( 
			"SELECT * FROM linkUsage ORDER BY id OFFSET %s FETCH FIRST %s ROW ONLY", 
			(offset, count)
			)
		# return self.cur.fetchall().toDict()
		return [
			{
				'id':link[0], 
				'date':link[1], 
				'link': link[2], 
				'msg': link[3]
				} 
			for link in self.cur.fetchall()
			]

	def addLink(self, msg, next):
		self.cur.execute(
			"INSERT INTO linkUsage (msg, next, timestamp) VALUES (%s, %s, NOW())",
			(msg, next,)
		)
		self.conn.commit()

db = Database()
