import os
import psycopg2
import gspread
from dotenv import load_dotenv

from oauth2client.service_account import ServiceAccountCredentials

load_dotenv(override=True)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('google-credentials.json', scope)
client = gspread.authorize(credentials)

DATABASE_URL = os.environ['DATABASE_URL']  
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

def load_data_from_google_sheets(spreadsheet_id, worksheet_name, table_name):
    sheet = client.open_by_key(spreadsheet_id)
    worksheet = sheet.worksheet(worksheet_name)

    data = worksheet.get_all_values()

    drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
    cursor.execute(drop_table_query)

    columns_with_types = [f"{col} VARCHAR(255)" for col in data[0]]
    create_table_query = f"""
        CREATE TABLE {table_name} (
            {', '.join(columns_with_types)}
        );
    """
    cursor.execute(create_table_query)

    insert_query = f"""
    INSERT INTO {table_name} ({', '.join(data[0])})
    VALUES ({', '.join(['%s' for _ in range(len(data[0]))])});
    """

    for row in data[1:]:  
        cursor.execute(insert_query, row)
    
    conn.commit()

    print(f"Data loaded into {table_name} successfully!")

if __name__ == "__main__":
    spreadsheet_id = "10KDw1cMOw4NaSXAJS8QObgpUnsfbWdj72ERZagWjoEs"
    
    # Load data for PLACES
    worksheet_name = "PLACES"
    table_name = "PLACES"
    load_data_from_google_sheets(spreadsheet_id, worksheet_name, table_name)
    
    # Load data for STALLS
    worksheet_name = "STALLS"
    table_name = "STALLS"
    load_data_from_google_sheets(spreadsheet_id, worksheet_name, table_name)
    
    # Load data for DISHES
    worksheet_name = "DISHES"
    table_name = "DISHES"
    load_data_from_google_sheets(spreadsheet_id, worksheet_name, table_name)

    cursor.close()
    conn.close()