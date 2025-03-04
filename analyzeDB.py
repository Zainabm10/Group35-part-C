from db_connector import db


def analyze_db():
    collections = db.list_collection_names()  # מביא את כל שמות הטבלאות (collections)
    if not collections:
        print("❌ No collections found in the database!")
        return

    print("📌 Analyzing Database:\n")
    for collection_name in collections:
        print(f"📂 Collection: {collection_name}")
        data = list(db[collection_name].find())  # מביא את כל הנתונים מהטבלה
        if data:
            for item in data:
                print(item)  # מדפיס את הנתונים
        else:
            print("⚠️ No data found.")
        print("\n" + "-" * 40 + "\n")  # מפריד בין הנתונים


if __name__ == "__main__":
    analyze_db()
