
from pymongo import MongoClient

def connectDataBase():
    client = MongoClient("mongodb://localhost:27017/")
    
    db = client['']  
    return db

def createDocument(collection, docId, docText, docTitle, docDate, docCat):
    document = {
        "_id": int(docId),
        "text": docText,
        "title": docTitle,
        "date": docDate,
        "category": docCat
    }
    collection.insert_one(document)
    print("Document created successfully.")

def updateDocument(collection, docId, docText, docTitle, docDate, docCat):
    collection.update_one(
        {"_id": int(docId)},
        {"$set": {
            "text": docText,
            "title": docTitle,
            "date": docDate,
            "category": docCat
        }}
    )
    print("Document updated successfully.")

def deleteDocument(collection, docId):
    collection.delete_one({"_id": int(docId)})
    print("Document deleted successfully.")

def getIndex(collection):
    index = {}
    cursor = collection.find()
    for doc in cursor:
        words = doc['text'].split()
        for word in words:
            cleaned_word = word.lower().strip(",.!?")
            if cleaned_word in index:
                if doc['title'] in index[cleaned_word]:
                    index[cleaned_word][doc['title']] += 1
                else:
                    index[cleaned_word][doc['title']] = 1
            else:
                index[cleaned_word] = {doc['title']: 1}
    sorted_index = {k: index[k] for k in sorted(index)}
    return sorted_index
