import os
from pymongo import MongoClient

# ==== CONFIG ====
IMAGE_FOLDER = './static/images'
MONGO_URI = 'mongodb+srv://YashmitSunkara:11132008@cluster0.vjgqqbm.mongodb.net/'  # replace with your actual URI if needed
DB_NAME = 'whois_db'
COLLECTION_NAME = 'Who is smarter?'       # you can change this per game mode
STARTING_ELO = 400
# ================

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Optional: clear collection before seeding
collection.delete_many({})

# Get all image files
for filename in os.listdir(IMAGE_FOLDER):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        person_name = os.path.splitext(filename)[0]  # derive name from filename
        doc = {
            "name": person_name,
            "filename": filename,
            "elo": STARTING_ELO,
            "wins": 0,
            "losses": 0
        }
        collection.insert_one(doc)

print(f"Inserted {collection.count_documents({})} records into '{COLLECTION_NAME}'")
