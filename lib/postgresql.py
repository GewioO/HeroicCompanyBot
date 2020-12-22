import psycopg2

cur = 0
con = 0

def databaseConnection():
      global con
      con = psycopg2.connect(
      database = "HeroicBot",
      user     = "postgres",
      password = "",
      host     = "localhost",
      port     = "5432"
)

def db_write_image(level, path):
      databaseActions("open")
      insertNewLevel(level, path)
      databaseActions("close")

def insertNewLevel(level, path):
      cur.execute("SELECT 'heroicStorage' FROM information_schema.tables WHERE table_schema='public'")
      rows = cur.fetchall()
      cur.execute("INSERT INTO heroicStorage (LEVEL, PATH, SERIAL_NUMBER) VALUES ("+level+","+path+",'1')")
      for row in rows:
            return row[0]

def databaseActions(state):
      if   state == "open":
            databaseConnection()
            global cur
            cur = con.cursor()
      elif state == "close":
            con.commit()  
            con.close()

db_write_image("1", "path")