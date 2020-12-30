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

def db_delete_photo(num):
  databaseActions("open")
  photo, ids = search_photo_by_id(num)
  for i in range(0,len(ids)):
    cur.execute("DELETE from heroic where ID='"+str(ids[i])+"';")
  databaseActions("close")
  if len(ids) < 1:
    ids = False
  return photo, ids

def db_check_path(path):
  databaseActions("open")
  photo = search_photo_by_path(path)
  databaseActions("close")
  return photo


def insertNewLevel(level, path):
  rows = fetch_all_rows()
  number = [];
  for row in rows:
    if row[2] == str(level) and row[1] == path:
      number.clear()
      number = False
      break
    else:
      number.append(row[0])
  if number:
    new_id = len(number)+1
    cur.execute("INSERT INTO heroic (ID, PATH, LEVEL) VALUES ("
            +str(new_id)+",'"+str(path)+"','"+str(level)+"')")
    return True
  elif number == False:
    return False
  else:
    cur.execute("INSERT INTO heroic (ID, PATH, LEVEL) VALUES ("
            +str(1)+",'"+str(path)+"','"+str(level)+"')")
    return True

def search_photo(level, count):
  rows = fetch_all_rows()
  iterator = 0
  ids = []
  images = []
  for row in rows:
    if row[2] == str(level):
        if count == "all":
          ids.append(row[0])
          images.append(row[1])
        elif iterator < 10:
          ids.append(row[0])
          images.append(row[1])
          iterator += 1
     
  return images, ids

def search_photo_by_id(num):
  rows = fetch_all_rows()
  ids = []
  images = []
  for row in rows:
    iterator = 0
    for i in range(0, len(num)):
      if iterator < len(num):
        if str(row[0]) == str(num[iterator]):
          ids.append(row[0])
          images.append(row[1])
      else:
        break
      iterator += 1
  return images, ids

def search_photo_by_path(path):
  rows = fetch_all_rows()
  image = False
  for row in rows:
    if row[1] == path:
      image = False
      break
    else:
      image = True
  
  return image

def fetch_all_rows():
  cur.execute("SELECT ID, PATH, LEVEL from heroic")
  rows = cur.fetchall()
  return rows

def databaseActions(state):
  if   state == "open":
    databaseConnection()
    global cur
    cur = con.cursor()
  elif state == "close":
    con.commit()  
    con.close()