#-------------------------------------------------------------------------
# AUTHOR: Matthew Plascencia
# FILENAME: db_connection_mongo.py
# SPECIFICATION: back end for adding documents to the database in mongdb.
# FOR: CS 5180- Assignment #2
# TIME SPENT: 5 hours
#-----------------------------------------------------------*/

from pymongo import MongoClient
import datetime
from collections import Counter
import re


def connectDataBase():
    client = MongoClient("mongodb://localhost:27017/")
    db_name = input("Enter the name of the database you want to manipulate: ")
    db = client[db_name]  
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

def generate_inverted_index(db, collection_name):
    collection = db[collection_name]
    inverted_index = {}

    documents = collection.find()
   
    for doc in documents:
        
        terms = re.findall(r'\b\w+\b', doc['text'].lower())  
        term_counts = Counter(terms)  
        
        for term, count in term_counts.items():
            if term not in inverted_index:
                inverted_index[term] = {}
            if doc['title'] in inverted_index[term]:
                inverted_index[term][doc['title']] += count
            else:
                inverted_index[term][doc['title']] = count

    
    sorted_inverted_index = {term: inverted_index[term] for term in sorted(inverted_index)}

    formatted_output = {}
    for term, docs in sorted_inverted_index.items():
        formatted_output[term] = ', '.join([f'{title}:{count}' for title, count in docs.items()])

    return formatted_output
