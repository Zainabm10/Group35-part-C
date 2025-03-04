import os
from pymongo import MongoClient
from dotenv import load_dotenv

# טען את קובץ ה-.env באופן מפורש
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path, override=True)

# קבל את ה-URI ממערכת הסביבה
DB_URI = os.getenv("DB_URI")

# בדיקה אם המשתנה נטען
if not DB_URI:
    raise ValueError("❌ Error: DB_URI is not set. Check your .env file.")

# התחברות למסד הנתונים
client = MongoClient(DB_URI)
db = client["StudentBudgetDB"]

def test_connection():
    try:
        print("Databases:", client.list_database_names())
        print("✅ MongoDB Connected Successfully! 🎉")
    except Exception as e:
        print("❌ Error connecting to MongoDB:", e)

if __name__ == "__main__":
    test_connection()
