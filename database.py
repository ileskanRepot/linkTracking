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
		ret = self.query(
			"SELECT * FROM linkUsage ORDER BY id OFFSET %s FETCH FIRST %s ROW ONLY",
		(offset, count)
		)
		return [
			{
				'id':link[0], 
				'date':link[1], 
				'link': link[2], 
				'msg': link[3]
				} 
			for link in ret[::-1]
			]

	def getDataLen(self):
		ret = self.query("SELECT count(*) FROM linkUsage ")
		return ret[0][0]

	def addLink(self, msg, next):
		self.execute("INSERT INTO linkUsage (msg, next, timestamp) VALUES (%s, %s, NOW())", (msg, next))

	def query(self, query, args = None, tries = 5):
		if tries <= 0:
			return -1
		try:
			self.cur.execute(
				query,
				args
			)
			return self.cur.fetchall()
		except Exception as ee:
			self.conn = self.connect()
			self.query(query, args, tries - 1)

	def execute(self, query, args = None, tries = 5):
		if tries <= 0:
			return -1
		try:
			self.cur.execute(
				query,
				args
			)
			self.conn.commit()
		except Exception as ee: 
			self.conn = self.connect()
			self.execute(query, args, tries - 1)


db = Database()
