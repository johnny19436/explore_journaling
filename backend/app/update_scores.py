import time
from app import mongo

def update_scores():
    while True:
        # Fetch all journals
        journals = mongo.db.journals.find()
        for journal in journals:
            # new_score = max(0, journal['score'] - 1)  # Decrease score by 10, ensure it doesn't go below 0
            mongo.db.journals.update_one({"_id": journal['_id']}, {"$set": {"score": journal['score'] - 1}})
        
        time.sleep(5760)  # Update scores every 20 seconds