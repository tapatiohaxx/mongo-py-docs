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
    words = docText.lower().split()  
    term_counts = Counter(words) 
    terms = [{'term': term, 'count': count, 'num_chars': len(term)} for term, count in term_counts.items()]

    final_document = {
        '_id': int(docId),  
        'text': docText,
        'title': docTitle,
        'date': datetime.datetime.strptime(docDate, '%Y-%m-%d'),
        'category': docCat,
        'terms': terms
    }
    result = col.insert_one(final_document)
    print(f"Document inserted with _id: {result.inserted_id}")


def updateDocument(col, docId, docText, docTitle, docDate, docCat):
    doc_id = int(docId)

    delete_result = col.delete_one({'_id': doc_id})
    if delete_result.deleted_count == 0:
        print(f"No document found with _id {docId}. Nothing was deleted.")
    else:
        print(f"Document with _id {docId} deleted.")
    new_document = {
        '_id': doc_id,
        'text': docText,
        'title': docTitle,
        'date': datetime.datetime.strptime(docDate, '%Y-%m-%d'),
        'category': docCat
    }
    # Insert the new document
    insert_result = col.insert_one(new_document)
    print(f"New document inserted with _id {insert_result.inserted_id}")

def deleteDocument(collection, docId):
    collection.delete_one({"_id": int(docId)})
    print("Document deleted successfully.")

def getIndex(col):
    
    documents = col.find()  
    inverted_index = {}

    for doc in documents:
        if 'text' in doc and 'title' in doc:  
            words = doc['text'].lower().split()  
            for word in words:
                if word not in inverted_index:
                    inverted_index[word] = {}
                if doc['title'] in inverted_index[word]:
                    inverted_index[word][doc['title']] += 1
                else:
                    inverted_index[word][doc['title']] = 1

   
    formatted_output = {}
    for term, titles in inverted_index.items():
        formatted_output[term] = ', '.join([f'{title}:{count}' for title, count in titles.items()])

    return formatted_output


