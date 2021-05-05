import os
import psycopg2



DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
# conn = psycopg2.connect(host="localhost", port = 5432, database="mylocaldb", user="postgres", password="1234567")

cur = conn.cursor()
print("Database opened successfully")

class BD1:

    def us_list():
        #cur.execute("""SELECT * FROM sample WHERE 1=1""")
        cur.execute("""SELECT * FROM users""")
        query_results = cur.fetchall()
        text = '\n'.join([', '.join(map(str, x)) for x in query_results])
        #print(len(query_results))
        #return (str(query_results))
        # return (123)
        return (str(text))



    def po_list():
        cur.execute("""SELECT * FROM posts""")
        query_results = cur.fetchall()
        text = '\n'.join([', '.join(map(str, x)) for x in query_results])
        return (str(text))
