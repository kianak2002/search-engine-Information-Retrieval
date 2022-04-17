from __future__ import unicode_literals
from hazm import stopwords_list
import json
import string
from parsivar import Normalizer
from parsivar import Tokenizer
from parsivar import FindStems


def read_file():
    document = []
    f = open('jsonfile.json', "r")
    data = json.loads(f.read())
    for item in data:
        document.append(data[item]['content'])
    f.close()
    return document


def delete_punctuation(document):
    document_new = []
    punctuations = string.punctuation
    punctuations += "".join(['،', '؟', '؛', '»', '«'])
    for text in document:
        text = text.translate(str.maketrans("", "", punctuations))
        document_new.append(text)
    return document_new


def normalize(document):
    document_new = []
    normalizer = Normalizer(statistical_space_correction=True)
    for text in document:
        text = normalizer.normalize(text)
        document_new.append(text)
    return document_new


def tokenize(document):
    document_new = []
    tokenizer = Tokenizer()
    for text in document:
        words = tokenizer.tokenize_words(text)
        document_new.append(words)
    return document_new


def stem(document):
    stemmer = FindStems()
    text_new = []
    document_new = []
    for text in document:
        print(len(text))
        for word in text:
            word = stemmer.convert_to_stem(word)
            text_new.append(word)
        document_new.append(text_new)
    return document


'''
first we check if the word is a stop word
if it is not then we save the docID and its index in it
'''


def positional_index(document):
    positional_index_list = {}
    for id in range(len(document)):
        for index in range(len(document[id])):
            word = document[id][index]
            if word not in stopwords_list():
                if word in positional_index_list:  # we have the word in positional index
                    doc_ID = positional_index_list.get(word)
                    check = False
                    for i in range(1, len(doc_ID)):
                        if id == doc_ID[i][0]:   # we have the doc id

                            doc_indexes = doc_ID[i][1]
                            doc_ID.remove((id, doc_indexes))  # first we delete it to update it
                            doc_indexes.append(index)  # we change the doc index
                            doc_ID.append((id, doc_indexes))  # update the docID
                            positional_index_list[word] = doc_ID  # we update the word positional index
                            check = True
                    if not check:  # we dont have the doc id
                        doc_indexes = []
                        doc_indexes.append(index)
                        doc_ID.append((id, doc_indexes))
                        positional_index_list[word] = doc_ID  # update the word positional index
                else:
                    doc_ID = []
                    doc_indexes = []
                    doc_indexes.append(index)
                    doc_ID.append(count)  # first index of this list is frequency of the word
                    doc_ID.append((id, doc_indexes))
                    positional_index_list[word] = doc_ID
    print(positional_index_list)

if __name__ == '__main__':
    doc = read_file()
    doc = delete_punctuation(doc)
    doc = normalize(doc)
    doc = tokenize(doc)
    doc = stem(doc)
    positional_index(doc)
