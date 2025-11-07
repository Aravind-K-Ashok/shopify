from app.database.database import engine

try:
    connection = engine.connect()
    print("✅ Connected to MySQL successfully!")
    connection.close()
except Exception as e:
    print("❌ Failed to connect:", e)
