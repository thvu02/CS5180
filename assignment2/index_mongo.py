#-------------------------------------------------------------------------
# AUTHOR: Trung Vu
# FILENAME: db_connection_mongo.py
# SPECIFICATION: Enable insertion, update, and deletion of documents into "documents" collection. Parse documents to tokenize and aggregate word occurrence information for each document.
# FOR: CS 5180- Assignment #2
# TIME SPENT: 6 hours
#-----------------------------------------------------------*/

from pymongo import MongoClient  # import mongo client to connect
from db_connection_mongo import *

if __name__ == '__main__':

    # Connecting to the database
    db = connectDataBase()

    # Creating a collection
    documents = db["documents"]

    #print a menu
    print("")
    print("######### Menu ##############")
    print("#a - Create a document")
    print("#b - Update a document")
    print("#c - Delete a document.")
    print("#d - Output the inverted index ordered by term.")
    print("#q - Quit")

    option = ""
    while option != "q":

          print("")
          option = input("Enter a menu choice: ")

          if (option == "a"):

              docId = input("Enter the ID of the document: ")
              docText = input("Enter the text of the document: ")
              docTitle = input("Enter the title of the document: ")
              docDate = input("Enter the date of the document: ")
              docCat = input("Enter the category of the document: ")

              createDocument(documents, docId, docText, docTitle, docDate, docCat)

          elif (option == "b"):

              docId = input("Enter the ID of the document: ")
              docText = input("Enter the text of the document: ")
              docTitle = input("Enter the title of the document: ")
              docDate = input("Enter the date of the document: ")
              docCat = input("Enter the category of the document: ")

              updateDocument(documents, docId, docText, docTitle, docDate, docCat)

          elif (option == "c"):

              docId = input("Enter the document ID to be deleted: ")

              deleteDocument(documents, docId)

          elif (option == "d"):

              index = getIndex(documents)
              print(index)

          elif (option == "q"):

               print("Leaving the application ... ")

          else:

               print("Invalid Choice.")