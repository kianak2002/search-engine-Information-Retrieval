from __future__ import unicode_literals
from hazm import stopwords_list
import json
import string
from parsivar import Normalizer
from parsivar import Tokenizer
from parsivar import FindStems
from collections import Counter


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
                        if id == doc_ID[i][0]:  # we have the doc id
                            count = doc_ID[0]
                            count += 1
                            doc_ID[0] = count
                            doc_indexes = doc_ID[i][1]
                            doc_ID.remove((id, doc_indexes))  # first we delete it to update it
                            doc_indexes.append(index)  # we change the doc index
                            doc_ID.append((id, doc_indexes))  # update the docID
                            positional_index_list[word] = doc_ID  # we update the word positional index
                            check = True
                    if not check:  # we dont have the doc id
                        count = doc_ID[0]
                        count += 1
                        doc_ID[0] = count
                        doc_indexes = []
                        doc_indexes.append(index)
                        doc_ID.append((id, doc_indexes))
                        positional_index_list[word] = doc_ID  # update the word positional index
                else:
                    count = 1
                    doc_ID = []
                    doc_indexes = []
                    doc_indexes.append(index)
                    doc_ID.append(count)  # first index of this list is frequency of the word
                    doc_ID.append((id, doc_indexes))
                    positional_index_list[word] = doc_ID
    return positional_index_list


'''
search the query in the positional index list and return the doc id
if it is just some words it check each of the and return a list of doc id's with the priority of frequency
'''


def search_query(positional_index_list):
    # query = input().split()  # now query is a list of words searched by user
    query = input()
    tokenizer = Tokenizer()
    query = tokenizer.tokenize_words(query)
    query = normalize(query)
    query = stem(query)

    quotation_first = False
    quotation_second = False
    id_s = []  # we save the doc id having the word and a frequency for the doc id of how many of the words it had
    id_s_not = []  # save the doc id's for "not" words
    print(query)
    for j in range(len(query)):
        word = query[j]
        if word[0] == '"':  # for the exact queries     first quotation
            quotation_first = True
            word = word[1:len(word)]
        if word[len(word) - 1] == '"':  # for the exact queries      last quotation
            quotation_second = True
            word = word[0:len(word)-1]

        if word in positional_index_list:
            doc_ID = positional_index_list.get(word)
            for i in range(1, len(doc_ID)):
                id = doc_ID[i][0]
                if j != 0 and query[j - 1] != '!':
                    id_s.append(id)
                elif j != 0 and query[j - 1] == '!':
                    id_s_not.append(id)
    id_s = sort_doc_id_s(id_s)
    id_s_not = sort_doc_id_s(id_s_not)
    list_result = subtract_list(id_s, id_s_not)
    print(list_result)


'''
in this function we sort the list by its frequency and then remove the duplicates
'''


def sort_doc_id_s(doc_list):
    doc_list = [key for key, value in Counter(doc_list).most_common()]
    return doc_list


'''
subtracts one list from the other list
'''


def subtract_list(list_first, list_second):
    res = []
    for item in list_first:
        if item not in list_second:
            res.append(item)
    return res


if __name__ == '__main__':
    doc = read_file()
    doc = delete_punctuation(doc)
    doc = normalize(doc)
    doc = tokenize(doc)
    doc = stem(doc)
    positional_index_list = positional_index(doc)
    print(positional_index_list)
    search_query(positional_index_list)
