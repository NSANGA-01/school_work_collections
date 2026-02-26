from pymongo import MongoClient
from werkzeug.security import generate_password_hash

client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["school_system"]

# List y'abantu dushaka kwinjiza
users_to_seed = [
    {
        "name": "System Admin",
        "email": "admin@school.com",
        "regNo": "ADMIN001",
        "class": None,
        "role": "admin",
        "password": "admin123"
    },
    {
        "name": "John Teacher",
        "email": "teacher@school.com",
        "regNo": "2",
        "class": None,
        "role": "teacher",
        "password": "teacher2"
    },
    {
        "name": "Jane teacher",
        "email": "student@school.com",
        "regNo": "3",
        "class": None,
        "role": "teacher",
        "password": "teacher3"
    }
]

for u in users_to_seed:
    # Reba niba user ihari mbere
    existing_user = db.users.find_one({"regNo": u["regNo"]})

    if existing_user:
        print(f"⚠ {u['name']} already exists. Skipping...")
        continue

    # Hash password mbere yo kubika
    u["password"] = generate_password_hash(u["password"])

    db.users.insert_one(u)
    print(f"✅ {u['name']} created successfully!")
