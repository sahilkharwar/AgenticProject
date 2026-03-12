from database import db

db.health_logs.insert_one({
"user_id": "123",
"date": "2026-03-12",
"notes": "Feeling good"
})

print("User inserted")