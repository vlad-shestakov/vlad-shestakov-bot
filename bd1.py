import params as p # Параметры приложения
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# DATABASE_URL = postgres://username:password@{DB_SERVICE_NAME}:5432/marketing
if p.STAND_TYPE == p.STAND_TYPE_PROD:
    DATABASE_URL = os.getenv("DATABASE_URL")
else:
    DATABASE_URL = os.getenv("DATABASE_URL_TEST")

conn = psycopg2.connect(DATABASE_URL, sslmode='allow') # sslmode = require / allow
# conn = psycopg2.connect(host="localhost", port = 5432, database="mylocaldb", user="user_name", password="pass")

cur = conn.cursor()

class BD1:
    # Класс доступа к БД

    def command_list():
        # Возвращает список команд бота
        sql_query = """ select c.id, c.command, c.command_hint, c.ord 
                          from COMMANDS c 
                         where c.active = 1
                         order by c.ord, c.id"""
        cur.execute(sql_query)
        query_results = cur.fetchall()
        text = ""
        for record in query_results:
            id_, command, command_hint, ord_ = record
            text = text + f"\n/{command} - {command_hint}"
        return text

    def get_command(command):
        # Возвращает список команд бота
        # print(f'command - {command}')
        result = None
        try:
            sql_query = """ SELECT c.message_head, c.message_text, c.image_link, c.image2_link
                            FROM COMMANDS c
                            WHERE c.active = 1
                              AND UPPER('/' || c.command) = UPPER(%(command)s)
                            LIMIT 1"""
            cur.execute(sql_query, {'command': command})
            result = cur.fetchone()
        except:
            pass
        return result

    def get_db_status():
        # Возвращает статус БД
        text = "Database opened successfully"
        return str(text)