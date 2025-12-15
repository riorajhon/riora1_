import pymongo
import random

def get_address(country_name, count=1):
    """Send country name and count, get addresses from MongoDB"""
    try:
        # Connect to MongoDB with authentication
        client = pymongo.MongoClient("mongodb://admin:wkrjk!20020415@localhost:27017/?authSource=admin")
        db = client['address']
        collection = db['addresses']
        
        # Find addresses with state False
        addresses = list(collection.find({"country": country_name, "state": False}).limit(count))
        
        # Update all selected addresses to True in one operation
        address_ids = [address["_id"] for address in addresses]
        collection.update_many({"_id": {"$in": address_ids}}, {"$set": {"state": True}})
        
        return [address["address"] for address in addresses]
            
    except Exception as e:
        return f"Error: {e}"
# Test
if __name__ == "__main__":
    print(get_address("germany", count=3))
   