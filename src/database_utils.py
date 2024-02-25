import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_URL = os.environ['DATABASE_URL']  
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

def get_places():
    cursor.execute("SELECT PLACE_NAME FROM PLACES;")
    data = cursor.fetchall()

    places = [place[0] for place in data]

    return places

def get_outlets(place):
    data = cursor.execute(f"SELECT STALL_NAME FROM STALLS S LEFT JOIN PLACES P ON S.PLACE_ID=P.PLACE_ID WHERE PLACE_NAME='{place}';")
    data = cursor.fetchall()

    stalls = [stall[0] for stall in data]
    
    return stalls