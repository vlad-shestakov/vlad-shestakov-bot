import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
# conn = psycopg2.connect(host="localhost", port = 5432, database="mylocaldb", user="postgres", password="1234567")

cur = conn.cursor()
print("Database opened successfully")

class BD1:
    """Класс доступа к БД"""

    def users_list(self):
        """Возвращает список пользователей"""
        cur.execute("""SELECT * FROM users""")
        query_results = cur.fetchall()
        text = '\n'.join([', '.join(map(str, x)) for x in query_results])
        return str(text)

    def posts_list(self):
        """Возвращает список постов пользователей"""
        cur.execute("""SELECT * FROM posts""")
        query_results = cur.fetchall()
        text = '\n'.join([', '.join(map(str, x)) for x in query_results])
        return str(text)
