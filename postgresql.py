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

