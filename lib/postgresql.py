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
  result = insertNewLevel(level, path)
  databaseActions("close")
  return result

def db_find_photo(level, count):
  databaseActions("open")
  photo = search_photo(level, count)
  databaseActions("close")
  return photo

def insertNewLevel(level, path):
  cur.execute("SELECT ID, PATH, LEVEL from heroic")
  number = 1;
  rows = cur.fetchall()
  for row in rows:
    number += 1
    if row[2] == str(level) and row[1] == path:
      number = False
      break
  if number:
    cur.execute("INSERT INTO heroic (ID, PATH, LEVEL) VALUES ("
            +str(number)+",'"+str(path)+"','"+str(level)+"')")
    return True
  else:
    return False

def search_photo(level, count):
  cur.execute("SELECT ID, PATH, LEVEL from heroic")
  rows = cur.fetchall()
  iterator = 0
  images = []
  for row in rows:
    if row[2] == str(level):
      images.append(row[1])
  
  return images

def databaseActions(state):
  if   state == "open":
    databaseConnection()
    global cur
    cur = con.cursor()
  elif state == "close":
    con.commit()  
    con.close()