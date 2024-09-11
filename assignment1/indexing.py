#-------------------------------------------------------------------------
# AUTHOR: Trung Vu
# FILENAME: indexing.py
# SPECIFICATION: Calculates document-term matrix for collection.csv dataset
# FOR: CS 5180- Assignment #1
# TIME SPENT: 4 hrs
#-----------------------------------------------------------*/

#Importing some Python libraries
import csv
import math # additional imported libraries

documents = []

#Reading the data in a csv file
with open('collection.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
         if i > 0:  # skipping the header
            documents.append (row[0])

#Conducting stopword removal for pronouns/conjunctions. Hint: use a set to define your stopwords.
#--> add your Python code here
# demonstrative pronouns, interrogative pronouns, personal pronouns, conjections
stopWords = {"I", "and", "She", "her", "They", "their"}
#Conducting stemming. Hint: use a dictionary to map word variations to their stem.
#--> add your Python code here
stemming = {"cat" : ["cats"],
            "love" : ["loves"],
            "dog" : ["dogs"]}

#Identifying the index terms.
#--> add your Python code here
terms = ["love", "cat", "dog"]

#Building the document-term matrix by using the tf-idf weights.
#--> add your Python code here

# remove stopwords from dataset
def remove_stopwords(stopWords, D):
    for index in range(len(D)):
      for word in stopWords:
        D[index] = D[index].replace(word, "")
      D[index] = " ".join(D[index].split()) # cleanup result to remove extra spaces
    return D

# conduct stemming on the dataset
def conduct_stemming(stemming, D):
    for index in range(len(D)):
      for stem in stemming.keys():
        for alt_word in stemming[stem]:
          if alt_word.casefold() in D[index].casefold():
            D[index] = D[index].replace(alt_word, stem) 
    return D

# return the term freq of the entire document
def get_tf(t, d):
    doc_length = len(d.split())
    lowercase_doc = d.casefold()
    term_freq = lowercase_doc.count(t.casefold())
    return round(term_freq / doc_length, 4)
    
# return the document frequency for the provided term
def get_df(t, D):
    df = 0
    for doc, num in zip(D,range(1,len(D)+1)):
        if t.casefold() in doc.casefold():
            df += 1
    return df

# return the inverse document freq: log scaled inverse fraction of documents (D) that contain term (T)
def get_idf(t,D):
    return round(math.log(len(D)/get_df(t,D),10), 4)

# return tf-idf
def get_tf_idf(t,d,D):
    return round(get_tf(t,d) * get_idf(t,D), 4)

def get_tf_idf_matrix(terms, documents):
  row = len(documents)+1
  col = len(terms)+1
  docTermMatrix = [[None]*col for i in range(row)] # add extra col and row for names

  # name the documents
  for i, doc_num in zip(range(1,row),range(1,len(documents)+1)):
     docTermMatrix[i][0] = f"D{doc_num}"

  # name the terms
  for j, term in zip(range(1,col),terms):
     docTermMatrix[0][j] = term

  # create the matrix
  D = conduct_stemming(stemming, remove_stopwords(stopWords, documents))
  for i,d in zip(range(1,row),D):
    for j,t in zip(range(1,col),terms):
      docTermMatrix[i][j] = get_tf_idf(t,d,D)
  return docTermMatrix

docTermMatrix = get_tf_idf_matrix(terms,documents)

#Printing the document-term matrix.
#--> add your Python code here
print(docTermMatrix)

# [[0.0, 0.12, 0.0], [0.0, 0.0, 0.09], [0.0, 0.06, 0.06]]