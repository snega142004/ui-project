import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="chat_db",   
    user="postgres",
    password="2004",
    port="5434"
)

cursor = conn.cursor()